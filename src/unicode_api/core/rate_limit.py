"""
This module implements rate limiting functionality for an API using the Generic Cell Rate Algorithm (GCRA)
with burst support. It leverages Redis as a backend for tracking request timestamps and managing locks.

Classes:
    RateLimitDecision:
        Represents a decision regarding rate limiting for a specific request, including details such as
        the IP address, request type, timestamps, and error messages.

    RateLimit:
        Implements the GCRA algorithm to enforce rate limiting for incoming API requests. It provides
        methods to validate requests, determine rate limit applicability, and manage rate limit state
        using Redis.

Constants:
    RATE_LIMIT_ROUTE_REGEX:
        A compiled regular expression used to determine if rate limiting applies to a specific route.

    rate_limit:
        An instance of the RateLimit class initialized with a Redis client.
"""

import logging
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import timedelta

from fastapi import Request
from redis.exceptions import LockError

from unicode_api.config.api_settings import get_settings
from unicode_api.core.redis_client import IRedisClient, redis
from unicode_api.core.util import (
    dtaware_fromtimestamp,
    format_timedelta_str,
    get_dict_report,
    get_duration_between_timestamps,
    get_time_until_timestamp,
    s,
)
from unicode_api.enums.request_type import RequestType

RATE_LIMIT_ROUTE_REGEX = re.compile(r"^\/v1\/blocks|characters|codepoints|planes")


@dataclass
class RateLimitDecision:
    """
    Represents a decision regarding rate limiting for a specific request.

    Attributes:
        ip (str): The IP address of the request origin.
        request_type (RequestType): The type of the request being evaluated.
        arrived_at (float): The timestamp when the request arrived.
        allowed_at (float): The timestamp when the request is allowed to proceed.
        new_tat (float): The new timestamp after which subsequent requests are allowed.
        error (str): An error message, if any, related to the rate limit decision.
        logger (logging.Logger): The logger instance used for logging rate limit decisions.

    Methods:
        __post_init__():
            Initializes the `error` attribute and sets up the logger instance.

        log() -> None:
            Logs the details of the rate limit decision, including whether the request
            was allowed or denied, and relevant timestamps and durations.
    """

    ip: str
    request_type: RequestType
    arrived_at: float
    allowed_at: float
    new_tat: float
    error: str = field(init=False)
    logger: logging.Logger = field(init=False)

    def __post_init__(self):
        """
        Post-initialization method for the dataclass.

        This method is automatically called after the dataclass is initialized.
        It sets up the `error` attribute as an empty string and initializes
        a logger instance for the "unicode_api.api" namespace.

        Attributes:
            error (str): A string to store error messages, initialized as an empty string.
            logger (logging.Logger): A logger instance for logging messages in the "unicode_api.api" namespace.
        """
        self.error = ""
        self.logger = logging.getLogger("unicode_api.api")

    def log(self) -> None:
        """
        Logs information about the rate limit status of a request.

        This method logs whether the request is allowed or denied based on the
        comparison of the `arrived_at` and `allowed_at` timestamps. It provides
        detailed information about the request, including the IP address,
        timestamps, and time-related calculations.

        Logs include:
        - Whether the request is allowed or denied.
        - The IP address of the requester.
        - The time the request arrived.
        - The time the request is allowed.
        - If allowed:
            - The new theoretical-arrival-time (TAT) and the duration until the limit resets.
        - If denied:
            - The remaining time until the rate limit expires.

        This method uses helper functions `_get_time_portion`,
        `get_duration_between_timestamps`, and `format_timedelta_str` to format
        and calculate time-related details.
        """
        allowed = self.arrived_at >= self.allowed_at
        self.logger.info(f"##### {'REQUEST ALLOWED' if allowed else 'REQUEST DENIED'} #####")
        self.logger.info(f"Request From...: {self.ip}")
        self.logger.info(f"Arrived At.....: {_get_time_portion(self.arrived_at)}")
        self.logger.info(f"Allowed At.....: {_get_time_portion(self.allowed_at)}")
        if allowed:
            new_tat = _get_time_portion(self.new_tat)
            dur_until_limit = get_duration_between_timestamps(self.allowed_at, self.arrived_at)
            time_until_limit = format_timedelta_str(dur_until_limit, precise=True)
            self.logger.info(f"New TAT........: {new_tat}, ({time_until_limit} from now)")
        else:
            dur_limit_remaining = get_duration_between_timestamps(self.arrived_at, self.allowed_at)
            time_limit_remaining = format_timedelta_str(dur_limit_remaining, precise=True)
            self.logger.info(f"Limit Expires..: {time_limit_remaining}")


class RateLimit:
    """
    RateLimit is a class that implements the Generic Cell Rate Algorithm (GCRA) with burst support
    to enforce rate limiting for incoming API requests. It uses Redis as a backend for tracking request
    timestamps and managing locks.

    Adapted for Python from this article:
    https://vikas-kumar.medium.com/rate-limiting-techniques-245c3a5e9cad

    Attributes:
        redis (IRedisClient): Redis client instance for managing rate limit data.
        logger (logging.Logger): Logger instance for logging rate limit events.
        settings (UnicodeApiSettings): Application settings containing rate limit configurations.

    Properties:
        is_test_env (bool): Indicates if the application is running in a test environment.
        rate (int): Maximum number of requests allowed per period.
        period (timedelta): Duration of the rate limit period.
        burst (int): Number of additional requests allowed in a burst.
        period_seconds (float): Duration of the rate limit period in seconds.
        period_milliseconds (float): Duration of the rate limit period in milliseconds.
        emission_interval_ms (timedelta): Time interval between allowed requests in milliseconds.
        delay_tolerance_ms (timedelta): Maximum delay tolerance for burst requests in milliseconds.

    Methods:
        validate_request(request: Request) -> RateLimitDecision:
            Validates an incoming request against the rate limit rules.
    """

    def __init__(self, redis: IRedisClient):
        """
        Initialize the RateLimit class.

        Args:
            redis (IRedisClient): An instance of a Redis client interface for interacting with the Redis database.
        """
        self.settings = get_settings()
        self.redis = redis
        self.logger = logging.getLogger("unicode_api.api")

    @property
    def is_test_env(self) -> bool:
        """
        Determine if the application is running in a test environment.

        Returns:
            bool: True if the application is in a test environment, False otherwise.
        """
        return self.settings.is_test

    @property
    def rate(self) -> int:
        """
        Retrieve the rate limit per period from the application settings.

        Returns:
            int: The maximum number of requests allowed per defined time period.
        """
        return self.settings.RATE_LIMIT_PER_PERIOD

    @property
    def period(self) -> timedelta:
        """
        Get the rate limit period.

        Returns:
            timedelta: The duration of the rate limit period, as defined by
            the RATE_LIMIT_PERIOD_SECONDS setting.
        """
        return self.settings.RATE_LIMIT_PERIOD_SECONDS

    @property
    def burst(self) -> int:
        """
        Retrieve the burst rate limit value.

        Returns:
            int: The maximum number of requests allowed in a burst.
        """
        return self.settings.RATE_LIMIT_BURST

    @property
    def period_seconds(self) -> float:
        """
        Calculate the duration of the rate limit period in seconds.

        Returns:
            float: The duration of the period in seconds.
        """
        return self.period / timedelta(seconds=1)

    @property
    def period_milliseconds(self) -> float:
        """
        Calculate the period in milliseconds.

        Returns:
            float: The duration of the period converted to milliseconds.
        """
        return self.period / timedelta(milliseconds=1)

    @property
    def emission_interval_ms(self) -> timedelta:
        """
        Calculate the emission interval in milliseconds.

        This method computes the time interval between emissions based on the
        rate and period in milliseconds. The interval is rounded to the nearest
        integer and returned as a timedelta object.

        Returns:
            timedelta: The time interval between emissions in milliseconds.
        """
        interval = round(self.period_milliseconds / float(self.rate))
        return timedelta(milliseconds=interval)

    @property
    def delay_tolerance_ms(self) -> timedelta:
        """
        Calculate the delay tolerance in milliseconds.

        This method computes the maximum allowable delay tolerance based on the
        emission interval and the burst capacity. The delay tolerance is the
        product of the emission interval and the burst size, returned as a
        timedelta object.

        Returns:
            timedelta: The calculated delay tolerance in milliseconds.
        """
        interval = self.emission_interval_ms / timedelta(milliseconds=1)
        return timedelta(milliseconds=(interval * self.burst))

    def validate_request(self, request: Request) -> RateLimitDecision:
        """
        Validates an incoming request and determines whether it should be rate-limited.

        This method checks the type of the request and applies rate-limiting rules
        based on the client's IP address and the request type. Requests for API endpoints
        are subject to rate limiting, while other request types (requests made during test
        case execution,requests from sites hosted on the same server, requests for static
        resources) are exempt from rate limiting.

        Args:
            request (Request): The incoming HTTP request to validate.

        Returns:
            RateLimitDecision: A decision object containing information about the
            rate-limiting status for the request.
        """
        ip = _get_client_ip_address(request)
        match request_type := self._check_for_simple_request_types(request, ip):
            case RequestType.TEST_REQUEST | RequestType.INTERNAL_REQUEST | RequestType.STATIC_RESOURCE:
                return RateLimitDecision(ip, request_type, 0, 0, 0)
            case _:
                return self._apply_rate_limiting(ip)

    def _check_for_simple_request_types(self, request: Request, ip: str) -> RequestType | None:
        if self.is_test_env and not _enable_rate_limit_feature_for_test(request):
            return RequestType.TEST_REQUEST
        if self._ip_is_internal(request, ip):  # pragma: no cover
            return RequestType.INTERNAL_REQUEST
        if not self._rate_limit_applies_to_route(request):  # pragma: no cover
            return RequestType.STATIC_RESOURCE
        return RequestType.NONE

    def _ip_is_internal(self, request: Request, client_ip: str) -> bool:  # pragma: no cover
        if any(host in client_ip for host in ["localhost", "127.0.0.1", "testserver"]):
            return True
        if self.settings.docker_ip_regex.search(client_ip):
            return True
        if "sec-fetch-site" in request.headers and request.headers["sec-fetch-site"] == "same-site":
            self._log_request_from_same_site(client_ip, request)
            return True
        return False

    def _log_request_from_same_site(self, ip: str, request: Request) -> None:  # pragma: no cover
        self.logger.info(f"##### BYPASS RATE LIMITING (SAME SITE, IP: {ip}) #####")
        for log in get_dict_report(request.headers):
            self.logger.info(log)

    def _rate_limit_applies_to_route(self, request: Request) -> bool:  # pragma: no cover
        return bool(RATE_LIMIT_ROUTE_REGEX.search(request.url.path))

    def _apply_rate_limiting(self, ip: str) -> RateLimitDecision:
        arrived_at = self.redis.time()
        self.redis.setnx(ip, "0")
        try:
            with self.redis.lock("lock:" + ip, blocking_timeout=5):
                tat = float(self.redis.get(ip) or 0)  # type: ignore  # noqa: PGH003
                allowed_at = self._get_allowed_at(tat)
                if arrived_at < allowed_at:
                    decision = RateLimitDecision(ip, RequestType.RATE_LIMITED_DENIED, arrived_at, allowed_at, 0)
                    decision.error = self._rate_limit_exceeded(ip, allowed_at)
                    return decision
                new_tat = self._get_new_tat(tat, arrived_at)
                self.redis.set(ip, new_tat)
                return RateLimitDecision(ip, RequestType.RATE_LIMITED_ALLOWED, arrived_at, allowed_at, new_tat)
        except LockError:  # pragma: no cover
            decision = RateLimitDecision(ip, RequestType.ERROR, arrived_at, 0, 0)
            decision.error = self._get_lock_error(ip)
            return decision

    def _get_allowed_at(self, tat: float) -> float:
        return (dtaware_fromtimestamp(tat) - self.delay_tolerance_ms).timestamp()

    def _get_new_tat(self, tat: float, arrived_at: float) -> float:
        return (dtaware_fromtimestamp(max(tat, arrived_at)) + self.emission_interval_ms).timestamp()

    def _rate_limit_exceeded(self, ip: str, allowed_at: float) -> str:
        limit_duration = get_time_until_timestamp(allowed_at)
        burst = f" (+{self.burst} request burst allowance)" if self.burst > 1 else ""
        detail = (
            f"API rate limit of {self.rate} requests{burst} in {round(self.period_seconds, 1)} "
            f"second{s(self.period_seconds)} exceeded for IP {ip}, "
            f"{format_timedelta_str(limit_duration, precise=True)} until limit is removed"
        )
        self.logger.debug(detail)
        return detail

    def _get_lock_error(self, client: str) -> str:  # pragma: no cover
        error = (
            f"An error occurred attempting to access rate limit data for IP {client} "
            f"(Error: Unable to acquire Redis lock for shared resource)."
        )
        self.logger.error(error)
        return error


def _get_client_ip_address(request: Request) -> str:
    if "x-forwarded-for" in request.headers:  # pragma: no cover
        return request.headers["x-forwarded-for"]
    return request.client.host if request.client else "localhost"


def _enable_rate_limit_feature_for_test(request: Request) -> bool:
    if "x-verify-rate-limiting" in request.headers:
        return request.headers["x-verify-rate-limiting"] == "true"
    if "access-control-request-headers" in request.headers:  # pragma: no cover
        ac_request_headers = request.headers["access-control-request-headers"]
        if isinstance(ac_request_headers, Mapping) and "x-verify-rate-limiting" in ac_request_headers:
            return ac_request_headers["x-verify-rate-limiting"] == "true"  # type: ignore[reportArgumentType]
    return False  # pragma: no cover


def _get_time_portion(ts: float) -> str:
    return dtaware_fromtimestamp(ts).time().strftime("%I:%M:%S.%f %p")


rate_limit = RateLimit(redis)
