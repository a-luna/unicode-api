from http import HTTPStatus
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from fastapi_redis_cache import FastApiRedisCache
from starlette.responses import RedirectResponse

from app.api.api_v1.api import router
from app.core.config import settings


APP_FOLDER = Path(__file__).parent
STATIC_FOLDER = APP_FOLDER.joinpath("static")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_VERSION}/openapi.json",
    docs_url=f"{settings.API_VERSION}/docs" if settings.ENV == "DEV" else None,
    redoc_url=None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3508",
        "http://10.0.1.52:3508",
        "http://localhost:3000",
        "http://10.0.1.52:3000",
        "https://base64-demo.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=str(STATIC_FOLDER)), name="static")


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=settings.REDIS_URL,
        response_header=settings.CACHE_HEADER,
    )


@app.get(f"{settings.API_VERSION}/docs", include_in_schema=False)
async def swagger_ui_html():
    return get_swagger_ui_html(
        title=f"{settings.PROJECT_NAME} - Swagger UI",
        openapi_url=app.openapi_url,
        swagger_favicon_url="/static/favicon.ico",
    )


@app.get("/", include_in_schema=False)
def get_api_root():
    api_docs_url = app.url_path_for("swagger_ui_html")
    return RedirectResponse(url=api_docs_url, status_code=int(HTTPStatus.PERMANENT_REDIRECT))


app.include_router(router, prefix=settings.API_VERSION)
