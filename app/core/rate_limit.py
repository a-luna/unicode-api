import logging
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import timedelta

from fastapi import Request
from redis.exceptions import LockError

from app.config.api_settings import get_settings
from app.core.redis_client import IRedisClient, redis
from app.core.util import (
    dtaware_fromtimestamp,
    format_timedelta_str,
    get_dict_report,
    get_duration_between_timestamps,
    get_time_until_timestamp,
    s,
)
from app.enums.request_type import RequestType

RATE_LIMIT_ROUTE_REGEX = re.compile(r"^\/v1\/blocks|characters|codepoints|planes")
DOCKER_IP_REGEX = re.compile(r"172\.17\.0\.\d{1,3}")


@dataclass
class RateLimitDecision:
    ip: str
    request_type: RequestType
    arrived_at: float
    allowed_at: float
    new_tat: float
    error: str = field(init=False)
    logger: logging.Logger = field(init=False)

    def __post_init__(self):
        self.error = ""
        self.logger = logging.getLogger("app.api")

    def log(self) -> None:
        allowed = self.arrived_at >= self.allowed_at
        self.logger.info(f"##### {'REQUEST ALLOWED' if allowed else 'REQUEST DENIED'} #####")
        self.logger.info(f"Request From...: {self.ip}")
        self.logger.info(f"Arrived At.....: {get_time_portion(self.arrived_at)}")
        self.logger.info(f"Allowed At.....: {get_time_portion(self.allowed_at)}")
        if allowed:
            new_tat = get_time_portion(self.new_tat)
            dur_until_limit = get_duration_between_timestamps(self.allowed_at, self.arrived_at)
            time_until_limit = format_timedelta_str(dur_until_limit, precise=True)
            self.logger.info(f"New TAT........: {new_tat}, ({time_until_limit} from now)")
        else:
            dur_limit_remaining = get_duration_between_timestamps(self.arrived_at, self.allowed_at)
            time_limit_remaining = format_timedelta_str(dur_limit_remaining, precise=True)
            self.logger.info(f"Limit Expires..: {time_limit_remaining}")


class RateLimit:
    """
    This is an implementation of the Generic Cell Rate Algorithm (GCRA) with burst.

    Adapted for Python from this article:
    https://vikas-kumar.medium.com/rate-limiting-techniques-245c3a5e9cad
    """

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

    def validate_request(self, request: Request) -> RateLimitDecision:
        client_ip = get_client_ip_address(request)
        request_type = self.apply_rate_limit_to_request(request, client_ip)
        if request_type:
            return RateLimitDecision(client_ip, request_type, 0, 0, 0)
        arrived_at = self.redis.time()
        self.redis.setnx(client_ip, "0")
        try:
            with self.redis.lock("lock:" + client_ip, blocking_timeout=5):
                tat = float(self.redis.get(client_ip) or 0)  # type: ignore  # noqa: PGH003
                allowed_at = self.get_allowed_at(tat)
                if arrived_at < allowed_at:
                    decision = RateLimitDecision(client_ip, RequestType.RATE_LIMITED_DENIED, arrived_at, allowed_at, 0)
                    decision.error = self.rate_limit_exceeded(client_ip, allowed_at)
                    return decision
                new_tat = self.get_new_tat(tat, arrived_at)
                self.redis.set(client_ip, new_tat)
                return RateLimitDecision(client_ip, RequestType.RATE_LIMITED_ALLOWED, arrived_at, allowed_at, new_tat)
        except LockError:  # pragma: no cover
            decision = RateLimitDecision(client_ip, RequestType.ERROR, arrived_at, 0, 0)
            decision.error = self.lock_error(client_ip)
            return decision

    def apply_rate_limit_to_request(self, request: Request, client_ip: str) -> RequestType | None:
        if self.settings.is_test:
            return None if enable_rate_limit_feature_for_test(request) else RequestType.TEST_REQUEST
        if self.client_ip_is_internal(request, client_ip):  # pragma: no cover
            return RequestType.INTERNAL_REQUEST
        return None if self.rate_limit_applies_to_route(request) else RequestType.STATIC_RESOURCE  # pragma: no cover

    def rate_limit_applies_to_route(self, request: Request) -> bool:  # pragma: no cover
        return bool(RATE_LIMIT_ROUTE_REGEX.search(request.url.path))

    def client_ip_is_internal(self, request: Request, client_ip: str) -> bool:  # pragma: no cover
        if any(host in client_ip for host in ["localhost", "127.0.0.1", "testserver"]):
            return True
        if DOCKER_IP_REGEX.search(client_ip):
            return True
        if "sec-fetch-site" in request.headers and request.headers["sec-fetch-site"] == "same-site":
            self.log_request_from_same_site(client_ip, request)
            return True
        return False

    def log_request_from_same_site(self, client_ip: str, request: Request) -> None:  # pragma: no cover
        self.logger.info(f"##### BYPASS RATE LIMITING (SAME SITE, IP: {client_ip}) #####")
        for log in get_dict_report(request.headers):
            self.logger.info(log)

    def get_allowed_at(self, tat: float) -> float:
        return (dtaware_fromtimestamp(tat) - self.delay_tolerance_ms).timestamp()

    def get_new_tat(self, tat: float, arrived_at: float) -> float:
        return (dtaware_fromtimestamp(max(tat, arrived_at)) + self.emission_interval_ms).timestamp()

    def rate_limit_exceeded(self, client, allowed_at: float) -> str:
        limit_duration = get_time_until_timestamp(allowed_at)
        burst = f" (+{self.burst} request burst allowance)" if self.burst > 1 else ""
        detail = (
            f"API rate limit of {self.rate} requests{burst} in {round(self.period_seconds, 1)} "
            f"second{s(self.period_seconds)} exceeded for IP {client}, "
            f"{format_timedelta_str(limit_duration, precise=True)} until limit is removed"
        )
        self.logger.debug(detail)
        return detail

    def lock_error(self, client) -> str:  # pragma: no cover
        error = (
            f"An error occurred attempting to access rate limit data for IP {client} "
            f"(Error: Unable to acquire Redis lock for shared resource)."
        )
        self.logger.error(error)
        return error


def get_client_ip_address(request: Request) -> str:
    if "x-forwarded-for" in request.headers:  # pragma: no cover
        return request.headers["x-forwarded-for"]
    return request.client.host if request.client else "localhost"


def enable_rate_limit_feature_for_test(request: Request) -> bool:
    if "x-verify-rate-limiting" in request.headers:
        return request.headers["x-verify-rate-limiting"] == "true"
    if "access-control-request-headers" in request.headers:  # pragma: no cover
        ac_request_headers = request.headers["access-control-request-headers"]
        if isinstance(ac_request_headers, Mapping) and "x-verify-rate-limiting" in ac_request_headers:
            return ac_request_headers["x-verify-rate-limiting"] == "true"  # type: ignore[reportArgumentType]
    return False  # pragma: no cover


def get_time_portion(ts: float) -> str:
    return dtaware_fromtimestamp(ts).time().strftime("%I:%M:%S.%f %p")


rate_limit = RateLimit(redis)
