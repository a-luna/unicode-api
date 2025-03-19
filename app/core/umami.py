import logging.config

import requests
from fastapi import Request

from app.config.api_settings import UnicodeApiSettings, get_settings
from app.constants import LOCALE_REGEX
from app.core.rate_limit import RateLimitDecision


def send_rate_limit_exceeded_event_to_umami(request: Request, decision: RateLimitDecision):
    event_data = get_default_umami_event_data(get_settings(), request)
    event_data["name"] = "Rate Limit Exceeded"
    event_data["data"] = get_default_user_data(request, decision)
    send_event_to_umami(request, decision, event_data)


def send_api_request_event_to_umami(request: Request, decision: RateLimitDecision):
    event_data = get_default_umami_event_data(get_settings(), request)
    event_data["name"] = request.url.path
    event_data["data"] = get_default_user_data(request, decision) | dict(request.query_params.items())
    send_event_to_umami(request, decision, event_data)


def get_default_umami_event_data(settings: UnicodeApiSettings, request: Request) -> dict:
    return {
        "hostname": settings.HOSTNAME,
        "language": request.headers.get("Accept-Language", "en-US"),
        "referrer": request.headers.get("Referer", ""),
        "screen": f"{request.headers.get('Screen-Width', '')}x{request.headers.get('Screen-Height', '')}",
        "title": f"{settings.PROJECT_NAME} API",
        "url": request.url.path,
        "website": settings.UMAMI_WEBSITE_ID,
    }


def get_default_user_data(request: Request, decision: RateLimitDecision) -> dict:
    language, variant = get_user_locale(request)
    return {"client_ip": decision.ip, "locale": f"{language}-{variant}", "language": language, "variant": variant}


def get_user_locale(request: Request) -> tuple[str, str]:
    header_accept_lang = request.headers.get("Accept-Language", "")
    if match := LOCALE_REGEX.match(header_accept_lang):
        return (match.group(1), match.group(2))
    return ("", "")


def send_event_to_umami(request: Request, decision: RateLimitDecision, event_data: dict):
    settings = get_settings()
    if settings.is_dev or settings.is_test:
        return
    umami_url = "https://aluna-umami.netlify.app/api/send"
    response = requests.post(
        umami_url,
        headers={
            "Content-Type": "application/json",
            "User-Agent": request.headers.get("User-Agent", requests.utils.default_user_agent()),
        },
        json={"payload": event_data, "type": "event"},
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger = logging.getLogger("app.api")
        logger.error(f"HTTP error occurred: {e}")
