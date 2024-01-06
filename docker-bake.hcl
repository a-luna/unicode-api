variable "GITHUB_SHA" {
  default = "latest"
}

variable "REDIS_PW" {
  default = ""
}

target "unicode-api" {
    dockerfile = "./Dockerfile"
    tags = ["ghcr.io/a-luna/unicode-api:${GITHUB_SHA}"]
    args = {
        ARG_ENV = "PROD"
        ARG_UNICODE_VERSION = "15.1.0"
        ARG_REDIS_HOST = "dokku-redis-vig-cache"
        ARG_REDIS_PORT = "6379"
        ARG_REDIS_DB = "1"
        ARG_REDIS_PW = "${REDIS_PW}"
        ARG_RATE_LIMIT_PER_PERIOD = "50"
        ARG_RATE_LIMIT_PERIOD_SECONDS = "60"
        ARG_RATE_LIMIT_BURST = "10"
        ARG_TEST_HEADER = "X-UnicodeAPI-Test"
    }
}
