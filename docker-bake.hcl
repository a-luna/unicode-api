variable "GITHUB_SHA" {
  default = "latest"
}

variable "REDIS_PW" {
  default = ""
}

variable "UNICODE_VERSION" {
  default = "15.0.0"
}

target "unicode-api" {
    dockerfile = "./Dockerfile"
    tags = ["ghcr.io/a-luna/unicode-api:${GITHUB_SHA}"]
    args = {
        REDIS_PW = "${REDIS_PW}"
        UNICODE_VERSION = "${UNICODE_VERSION}"
    }
}
