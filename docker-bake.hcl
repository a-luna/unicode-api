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
        ENV = "PROD"
        UNICODE_VERSION = "15.1.0"
        REDIS_HOST = "dokku-redis-vig-cache"
        REDIS_PORT = "6379"
        REDIS_DB = "1"
        REDIS_PW = "${REDIS_PW}"
        RATE_LIMIT_PER_PERIOD = "50"
        RATE_LIMIT_PERIOD_SECONDS = "60"
        RATE_LIMIT_BURST = "10"
        TEST_HEADER = "X-UnicodeAPI-Test"
    }
}
