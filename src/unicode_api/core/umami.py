"""
This module provides integration with Umami analytics for tracking API usage events.

Functions:
    send_rate_limit_exceeded_event_to_umami(request: Request, ip: str):
        Sends a "rate_limit_exceeded" event to Umami analytics when a client exceeds the API rate limit.

    send_api_request_event_to_umami(request: Request, ip: str):
        Sends an API request event to Umami analytics, capturing route, user, and query parameter data.
"""

import logging
from typing import Any

import requests
from fastapi import Request

from unicode_api.config.api_settings import UnicodeApiSettings, get_settings
from unicode_api.constants import LOCALE_REGEX
from unicode_api.core.cache import cached_data


def send_rate_limit_exceeded_event_to_umami(request: Request, ip: str):
    """
    Sends a "rate_limit_exceeded" event to Umami analytics.

    This function constructs the appropriate event data, including default event and user information,
    and sends it to Umami for tracking when a rate limit has been exceeded for a given request.

    Args:
        request (Request): The incoming HTTP request object.
        ip (str): The IP address of the client that triggered the rate limit.

    Returns:
        None
    """
    event_data = _get_default_umami_event_data(get_settings(), request)
    event_data["name"] = "rate_limit_exceeded"
    event_data["data"] = _get_default_user_data(request, ip)
    _send_event_to_umami(request, event_data)


def send_api_request_event_to_umami(request: Request, ip: str):
    """
    Sends an API request event to Umami analytics.

    This function collects relevant event data from the incoming API request, including route information,
    user data, and query parameters, then sends the event to Umami for tracking.

    Args:
        request (Request): The incoming API request object.
        ip (str): The IP address of the client making the request.

    Returns:
        None
    """
    api_route, path_param = cached_data.get_api_route_from_requested_path(request.url.path)
    event_data = _get_default_umami_event_data(get_settings(), request)
    event_data["name"] = api_route["name"]
    event_data["data"] = _get_default_user_data(request, ip)
    event_data["data"]["api_endpoint"] = api_route["path"]
    if path_param:
        event_data["data"]["path_param"] = path_param
    event_data["data"].update(dict(request.query_params.items()))
    _send_event_to_umami(request, event_data)


def _get_default_umami_event_data(settings: UnicodeApiSettings, request: Request) -> dict[str, Any]:
    return {
        "hostname": settings.HOSTNAME,
        "language": request.headers.get("Accept-Language", "en-US"),
        "referrer": request.headers.get("Referer", ""),
        "screen": f"{request.headers.get('Screen-Width', '')}x{request.headers.get('Screen-Height', '')}",
        "title": f"{settings.project_name} API",
        "url": f"{request.url.path}{'?' if request.url.query else ''}{request.url.query}",
        "website": settings.UMAMI_WEBSITE_ID,
    }


def _get_default_user_data(request: Request, ip: str) -> dict[str, Any]:
    language, variant = _get_user_locale(request)
    return {"client_ip": ip, "locale": f"{language}-{variant}", "language": language, "variant": variant}


def _get_user_locale(request: Request) -> tuple[str, str]:
    if match := LOCALE_REGEX.match(request.headers.get("Accept-Language", "")):  # pragma: no cover
        return (match.group(1), match.group(2))
    return ("", "")


def _send_event_to_umami(request: Request, event_data: dict[str, Any]):  # pragma: no cover
    settings = get_settings()
    if settings.is_dev or settings.is_test:
        return
    response = requests.post(
        settings.UMAMI_API_URL,
        headers={
            "Content-Type": "application/json",
            "User-Agent": request.headers.get("User-Agent", requests.utils.default_user_agent()),
        },
        json={"payload": event_data, "type": "event"},
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger = logging.getLogger("unicode_api.api")
        logger.error(f"HTTP error occurred: {e}")
