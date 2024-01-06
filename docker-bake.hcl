variable "GITHUB_SHA" {
  default = "latest"
}

variable "REDIS_PW" {
  default = ""
}

variable "TEST1" {
  default = "NOT_SECRET1"
}

variable "TEST2" {
  default = "NOT_SECRET2"
}

target "unicode-api" {
    dockerfile = "./Dockerfile"
    tags = ["ghcr.io/a-luna/unicode-api:${GITHUB_SHA}"]
    args = {
        ENV="PROD"
        UNICODE_VERSION="14.0.0"
        REDIS_HOST="dokku-redis-vig-cache"
        REDIS_PORT="6379"
        REDIS_DB="1"
        REDIS_PW="${REDIS_PW}"
        RATE_LIMIT_PER_PERIOD="45"
        RATE_LIMIT_PERIOD_SECONDS="55"
        RATE_LIMIT_BURST="5"
        TEST_HEADER="X-UnicodeAPI-Test"
        TEST1="${TEST1}"
        TEST2="${TEST2}"
    }
}
