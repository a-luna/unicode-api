from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.redis_client import redis


def check_rate_limit(request: Request):
    client_ip = request.client.host if request.client else ""
    rate_limit_exceeded, timestamp = redis.rate_limit_exceeded(client_ip)
    if rate_limit_exceeded:
        return JSONResponse(content="API rate limit exceeded", status_code=int(HTTPStatus.TOO_MANY_REQUESTS))
