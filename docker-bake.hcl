variable "GITHUB_SHA" {
  default = "latest"
}

variable "REDIS_PW" {
  default = ""
}

variable "ENV" {
  default = ""
}

variable "UNICODE_VERSION" {
  default = ""
}

variable "UMAMI_WEBSITE_ID" {
  default = ""
}

target "unicode-api" {
    dockerfile = "./Dockerfile"
    tags = ["ghcr.io/a-luna/unicode-api:${GITHUB_SHA}"]
    args = {
        ENV="${ENV}"
        UNICODE_VERSION="${UNICODE_VERSION}"
        HOSTNAME="unicode-api.aaronluna.dev"
        REDIS_HOST="dokku-redis-vig-cache"
        REDIS_PORT="6379"
        REDIS_DB="1"
        REDIS_PW="${REDIS_PW}"
        RATE_LIMIT_PER_PERIOD="50"
        RATE_LIMIT_PERIOD_SECONDS="60"
        RATE_LIMIT_BURST="10"
        UMAMI_WEBSITE_ID="${UMAMI_WEBSITE_ID}"
    }
}
