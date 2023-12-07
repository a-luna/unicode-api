import logging
import os
import re
from datetime import datetime

from fastapi import Request
from redis.exceptions import LockError

from app.core.config import get_settings
from app.core.redis_client import RedisClient, redis
from app.core.result import Result
from app.core.util import get_duration_from_timestamp

RATE_LIMIT_ROUTE_REGEX = re.compile(r"^\/v1\/blocks|characters|planes")


class RateLimit:
    """
    RateLimit class
    """

    def __init__(self, redis: RedisClient):
        settings = get_settings()
        self.limit = settings.RATE_LIMIT_PER_PERIOD
        self.period = settings.RATE_LIMIT_PERIOD_SECONDS
        self.burst = settings.RATE_LIMIT_BURST
        self.logger = logging.getLogger("app.api")
        self.redis = redis

    @property
    def emission_interval(self) -> int:
        return round(int(self.period.total_seconds()) / float(self.limit))

    def is_exceeded(self, request: Request) -> Result[None]:
        """
        This is an implementation of the Genetic Cell Rate Algorithm (GCRA) with burst.

        Adapted for Python from this article:
        https://vikas-kumar.medium.com/rate-limiting-techniques-245c3a5e9cad
        """
        if rate_limit_is_not_required(request):
            return Result.Ok()
        client_ip = request.client.host
        arrived_at = datetime.now().timestamp()
        self.redis.setnx(client_ip, 0)
        try:
            with self.redis.lock("lock:" + client_ip, blocking_timeout=5):
                tat = float(self.redis.get(client_ip) or 0)  # type: ignore  # noqa: PGH003
                allowed_at = tat - (self.emission_interval * self.burst)
                if arrived_at < allowed_at:
                    return self.rate_limit_exceeded(client_ip, allowed_at)
                new_tat = max(tat, arrived_at) + self.emission_interval
                self.redis.set(client_ip, new_tat)
                return self.request_allowed(client_ip)
        except LockError:  # pragma: no cover
            return self.lock_error(client_ip)

    def rate_limit_exceeded(self, client, allowed_at: float) -> Result[str]:
        limit_duration = get_duration_from_timestamp(allowed_at)
        error = (
            f"API rate limit of {self.limit} requests in {self.period.seconds} seconds exceeded for IP {client}, "
            f"{limit_duration} until limit is removed"
        )
        self.logger.info(error)
        return Result.Fail(error)

    def request_allowed(self, client) -> Result[str]:
        self.logger.info(f"Request allowed for IP: {client}")
        return Result.Ok()

    def lock_error(self, client) -> Result[str]:
        error = (
            f"An error occurred attempting to access rate limit data for IP {client} "
            f"(Error: Unable to acquire Redis lock for shared resource)."
        )
        self.logger.info(error)
        return Result.Fail(error)


def rate_limit_is_not_required(request: Request):
    return testing(request) or requested_route_is_not_rate_limited(request) or client_ip_address_is_missing(request)


def testing(request: Request) -> bool:
    test_header = os.environ.get("TEST_HEADER", "").lower()
    return (
        test_header in request.headers or test_header in request.headers.get("access-control-request-headers", [])
        if test_header
        else False
    )


def requested_route_is_not_rate_limited(request: Request):
    return not RATE_LIMIT_ROUTE_REGEX.search(request.url.path)


def client_ip_address_is_missing(request):
    return not request.client


rate_limit = RateLimit(redis)
