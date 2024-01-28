import logging
import re
from dataclasses import dataclass
from datetime import timedelta

from fastapi import Request
from redis.exceptions import LockError

from app.config.api_settings import get_settings
from app.core.redis_client import IRedisClient, redis
from app.core.result import Result
from app.core.util import (
    dtaware_fromtimestamp,
    format_timedelta_str,
    get_duration_between_timestamps,
    get_time_until_timestamp,
)

RATE_LIMIT_ROUTE_REGEX = re.compile(r"^\/v1\/blocks|characters|planes")


@dataclass
class RateLimitDecision:
    ip: str
    arrived_at: float
    allowed_at: float
    new_tat: float

    def log(self) -> None:
        decision = (
            "RATE LIMIT DECISION:  "
            f"(IP: {self.ip})  "
            f"(Allowed: {self.arrived_at >= self.allowed_at})  "
            f"(Arrived At: {get_time_portion(self.arrived_at)})  "
            f"(Allowed At: {get_time_portion(self.allowed_at)})  "
        )
        if self.arrived_at < self.allowed_at:
            limit_duration = get_duration_between_timestamps(self.arrived_at, self.allowed_at)
            decision += f"({format_timedelta_str(limit_duration, precise=True)} Until Next Request Allowed)"

        else:
            time_until_limit = get_duration_between_timestamps(self.allowed_at, self.arrived_at)
            decision += (
                f"(New TAT: {get_time_portion(self.new_tat)}, "
                f"{format_timedelta_str(time_until_limit, precise=True)} from now)"
            )
        logging.getLogger("app.api").info(decision)


class RateLimit:
    def __init__(self, redis: IRedisClient):
        self.settings = get_settings()
        self.rate = self.settings.RATE_LIMIT_PER_PERIOD
        self.period = self.settings.RATE_LIMIT_PERIOD_SECONDS
        self.burst = self.settings.RATE_LIMIT_BURST
        self.redis = redis
        self.logger = logging.getLogger("app.api")

    @property
    def period_seconds(self) -> float:
        return self.period / timedelta(seconds=1)

    @property
    def period_milliseconds(self) -> float:
        return self.period / timedelta(milliseconds=1)

    @property
    def emission_interval_ms(self) -> timedelta:
        interval = round(self.period_milliseconds / float(self.rate))
        return timedelta(milliseconds=interval)

    @property
    def delay_tolerance_ms(self) -> timedelta:
        interval = self.emission_interval_ms / timedelta(milliseconds=1)
        return timedelta(milliseconds=(interval * self.burst))

    def is_exceeded(self, request: Request) -> Result[None]:
        """
        This is an implementation of the Generic Cell Rate Algorithm (GCRA) with burst.

        Adapted for Python from this article:
        https://vikas-kumar.medium.com/rate-limiting-techniques-245c3a5e9cad
        """
        if not self.apply_rate_limit_to_request(request):
            return Result.Ok()
        client_ip = request.client.host if request.client else "localhost"
        arrived_at = self.redis.time()
        self.redis.setnx(client_ip, "0")
        try:
            with self.redis.lock("lock:" + client_ip, blocking_timeout=5):
                tat = float(self.redis.get(client_ip) or 0)  # type: ignore  # noqa: PGH003
                allowed_at = self.get_allowed_at(tat)
                if arrived_at < allowed_at:
                    RateLimitDecision(client_ip, arrived_at, allowed_at, 0).log()
                    return self.rate_limit_exceeded(client_ip, allowed_at)
                new_tat = self.get_new_tat(tat, arrived_at)
                RateLimitDecision(client_ip, arrived_at, allowed_at, new_tat).log()
                self.redis.set(client_ip, new_tat)
                return self.request_allowed(client_ip)
        except LockError:  # pragma: no cover
            return self.lock_error(client_ip)

    def apply_rate_limit_to_request(self, request: Request):
        if self.settings.is_test:
            return enable_rate_limit_feature_for_test(request)
        return request_origin_is_external(request) and requested_route_is_rate_limited(request)

    def get_allowed_at(self, tat: float) -> float:
        return (dtaware_fromtimestamp(tat) - self.delay_tolerance_ms).timestamp()

    def get_new_tat(self, tat: float, arrived_at: float) -> float:
        return (dtaware_fromtimestamp(max(tat, arrived_at)) + self.emission_interval_ms).timestamp()

    def rate_limit_exceeded(self, client, allowed_at: float) -> Result[None]:
        limit_duration = get_time_until_timestamp(allowed_at)
        burst = f" (+{self.burst} request burst allowance)" if self.burst > 1 else ""
        error = (
            f"API rate limit of {self.rate} requests{burst} in {round(self.period_seconds, 1)} "
            f"second{'s' if self.period_seconds > 1 else ''} exceeded for IP {client}, "
            f"{format_timedelta_str(limit_duration, precise=True)} until limit is removed"
        )
        self.logger.info(error)
        return Result.Fail(error)

    def request_allowed(self, client) -> Result[None]:
        self.logger.info(f"Request allowed for IP: {client}")
        return Result.Ok()

    def lock_error(self, client) -> Result[None]:  # pragma: no cover
        error = (
            f"An error occurred attempting to access rate limit data for IP {client} "
            f"(Error: Unable to acquire Redis lock for shared resource)."
        )
        self.logger.error(error)
        return Result.Fail(error)


def enable_rate_limit_feature_for_test(request: Request) -> bool:
    if "x-verify-rate-limiting" in request.headers:
        return request.headers["x-verify-rate-limiting"] == "true"
    if "access-control-request-headers" in request.headers:  # pragma: no cover
        ac_request_headers = request.headers["access-control-request-headers"]
        if isinstance(ac_request_headers) == dict and "x-verify-rate-limiting" in ac_request_headers:
            return ac_request_headers["x-verify-rate-limiting"] == "true"
    return False  # pragma: no cover


def request_origin_is_external(request: Request) -> bool:
    if request.client.host in ["localhost", "127.0.0.1", "testserver"]:
        return False
    if "sec-fetch-site" in request.headers:
        return request.headers["sec-fetch-site"] != "same-site"
    return True


def requested_route_is_rate_limited(request: Request):
    return RATE_LIMIT_ROUTE_REGEX.search(request.url.path)


def get_time_portion(ts: float) -> str:
    return dtaware_fromtimestamp(ts).time().strftime("%I:%M:%S.%f %p")


rate_limit = RateLimit(redis)
