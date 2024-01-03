FROM python:3.11

ENV ENV=PROD
ENV TEST_HEADER=X-UnicodeAPI-Test
ENV RATE_LIMIT_PER_PERIOD=50
ENV RATE_LIMIT_PERIOD_SECONDS=60
ENV RATE_LIMIT_BURST=10
ENV REDIS_HOST=dokku-redis-vig-cache
ENV REDIS_PORT=6379
ENV REDIS_DB=1

ARG REDIS_PW
ENV REDIS_PW=${REDIS_PW}

ARG UNICODE_VERSION
ENV UNICODE_VERSION=${UNICODE_VERSION}

WORKDIR /code
RUN pip install -U pip setuptools wheel
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 80
COPY ./app /code/app 
RUN PYTHONPATH=/code/. python /code/./app/data/scripts/get_prod_data.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
