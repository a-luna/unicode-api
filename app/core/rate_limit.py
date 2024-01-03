import logging
import re
from dataclasses import dataclass, field
from datetime import timedelta

from fastapi import Request
from redis.exceptions import LockError

from app.config import get_settings
from app.core.redis_client import IRedisClient, redis
from app.core.result import Result
from app.core.util import dtaware_fromtimestamp, get_duration_between_timestamps, get_time_until_timestamp

RATE_LIMIT_ROUTE_REGEX = re.compile(r"^\/v1\/blocks|characters|planes")


@dataclass
class RateLimitDecision:
    ip: str
    tat: float
    new_tat: float
    arrived_at: float
    allowed_at: float
    logger: logging.Logger = field(init=False, default=None)

    def __post_init__(self):
        self.logger = logging.getLogger("app.api")

    def log(self) -> str:
        decision = (
            "RATE LIMIT DECISION:  "
            f"(IP: {self.ip})  "
            f"(Allowed: {self.arrived_at >= self.allowed_at})  "
            f"(Arrived At: {get_time_portion(self.arrived_at)})  "
            f"(Allowed At: {get_time_portion(self.allowed_at)})  "
        )
        if self.arrived_at < self.allowed_at:
            decision += (
                f"({get_duration_between_timestamps(self.arrived_at, self.allowed_at)}) Until Next Request Allowed)"
            )
        else:
            decision += (
                f"(New TAT: {get_time_portion(self.new_tat)}, "
                f"{get_duration_between_timestamps(self.allowed_at, self.arrived_at)} from now)"
            )
        self.logger.debug(decision)


class RateLimit:
    def __init__(self, redis: IRedisClient):
        self.settings = get_settings()
        self.logger = logging.getLogger("app.api")
        self.rate = self.settings.RATE_LIMIT_PER_PERIOD
        self.period = self.settings.RATE_LIMIT_PERIOD_SECONDS
        self.burst = self.settings.RATE_LIMIT_BURST
        self.redis = redis

    @property
    def emission_interval(self) -> timedelta:
        interval = round((self.period.total_seconds() * 1000) / float(self.rate))
        return timedelta(milliseconds=interval)

    @property
    def delay_tolerance(self) -> timedelta:
        interval = self.emission_interval.total_seconds() * 1000
        return timedelta(milliseconds=(interval * self.burst))

    def is_exceeded(self, request: Request) -> Result[None]:
        """
        This is an implementation of the Generic Cell Rate Algorithm (GCRA) with burst.

        Adapted for Python from this article:
        https://vikas-kumar.medium.com/rate-limiting-techniques-245c3a5e9cad
        """
        if self.rate_limit_is_not_required(request):
            return Result.Ok()
        client_ip = request.client.host
        arrived_at = self.redis.time()
        self.redis.setnx(client_ip, 0)
        try:
            with self.redis.lock("lock:" + client_ip, blocking_timeout=5):
                tat = float(self.redis.get(client_ip) or 0)  # type: ignore  # noqa: PGH003
                allowed_at = self.get_allowed_at(tat)
                if arrived_at < allowed_at:
                    RateLimitDecision(client_ip, tat, 0, arrived_at, allowed_at).log()
                    return self.rate_limit_exceeded(client_ip, allowed_at)
                new_tat = self.get_new_tat(tat, arrived_at)
                RateLimitDecision(client_ip, tat, new_tat, arrived_at, allowed_at).log()
                self.redis.set(client_ip, new_tat)
                return self.request_allowed(client_ip)
        except LockError:  # pragma: no cover
            return self.lock_error(client_ip)

    def rate_limit_is_not_required(self, request: Request):
        if self.settings.is_prod:  # pragma: no cover
            return requested_route_is_not_rate_limited(request) or client_ip_address_is_missing(request)
        if self.settings.is_dev:  # pragma: no cover
            return False
        return current_test_does_not_verify_rate_limit(request)

    def get_allowed_at(self, tat: float) -> float:
        return (dtaware_fromtimestamp(tat) - self.delay_tolerance).timestamp()

    def get_new_tat(self, tat: float, arrived_at: float) -> float:
        return (dtaware_fromtimestamp(max(tat, arrived_at)) + self.emission_interval).timestamp()

    def rate_limit_exceeded(self, client, allowed_at: float) -> Result[str]:
        limit_duration = get_time_until_timestamp(allowed_at)
        burst = f" (+{self.burst} request burst allowance)" if self.burst > 1 else ""
        error = (
            f"API rate limit of {self.rate} requests{burst} in {self.period.seconds} seconds exceeded for IP {client}, "
            f"{limit_duration} until limit is removed"
        )
        self.logger.info(error)
        return Result.Fail(error)

    def request_allowed(self, client) -> Result[str]:
        self.logger.info(f"Request allowed for IP: {client}")
        return Result.Ok()

    def lock_error(self, client) -> Result[str]:  # pragma: no cover
        error = (
            f"An error occurred attempting to access rate limit data for IP {client} "
            f"(Error: Unable to acquire Redis lock for shared resource)."
        )
        self.logger.error(error)
        return Result.Fail(error)


def current_test_does_not_verify_rate_limit(request: Request) -> bool:
    return not (
        request.headers["x-verify-rate-limiting"] == "true"
        if "x-verify-rate-limiting" in request.headers
        else request.headers.get("access-control-request-headers", [])["x-verify-rate-limiting"] == "true"
        if "x-verify-rate-limiting" in request.headers.get("access-control-request-headers", [])
        else False
    )


def requested_route_is_not_rate_limited(request: Request):  # pragma: no cover
    return not RATE_LIMIT_ROUTE_REGEX.search(request.url.path)


def client_ip_address_is_missing(request):  # pragma: no cover
    return not request.client


def get_time_portion(ts: float) -> str:
    return dtaware_fromtimestamp(ts).time().strftime("%I:%M:%S.%f %p")


rate_limit = RateLimit(redis)
