FROM python:3.12
SHELL ["/bin/bash", "-c"]

ARG ENV
ARG UNICODE_VERSION
ARG HOSTNAME
ARG REDIS_HOST
ARG REDIS_PORT
ARG REDIS_DB
ARG REDIS_PW
ARG RATE_LIMIT_PER_PERIOD
ARG RATE_LIMIT_PERIOD_SECONDS
ARG RATE_LIMIT_BURST
ARG UMAMI_WEBSITE_ID
ARG TEST_HEADER

ENV ENV=${ENV}
ENV UNICODE_VERSION=${UNICODE_VERSION}
ENV HOSTNAME=${HOSTNAME}
ENV REDIS_HOST=${REDIS_HOST}
ENV REDIS_PORT=${REDIS_PORT}
ENV REDIS_DB=${REDIS_DB}
ENV REDIS_PW=${REDIS_PW}
ENV RATE_LIMIT_PER_PERIOD=${RATE_LIMIT_PER_PERIOD}
ENV RATE_LIMIT_PERIOD_SECONDS=${RATE_LIMIT_PERIOD_SECONDS}
ENV RATE_LIMIT_BURST=${RATE_LIMIT_BURST}
ENV UMAMI_WEBSITE_ID=${UMAMI_WEBSITE_ID}

WORKDIR /code

RUN touch /code/.env
RUN echo "ENV=$ENV" >> /code/.env
RUN echo "PYTHONPATH=." >> /code/.env
RUN echo "UNICODE_VERSION=$UNICODE_VERSION" >> /code/.env
RUN echo "HOSTNAME=$HOSTNAME" >> /code/.env
RUN echo "REDIS_HOST=$REDIS_HOST" >> /code/.env
RUN echo "REDIS_PORT=$REDIS_PORT" >> /code/.env
RUN echo "REDIS_DB=$REDIS_DB" >> /code/.env
RUN echo "REDIS_PW=$REDIS_PW" >> /code/.env
RUN echo "RATE_LIMIT_PER_PERIOD=$RATE_LIMIT_PER_PERIOD" >> /code/.env
RUN echo "RATE_LIMIT_PERIOD_SECONDS=$RATE_LIMIT_PERIOD_SECONDS" >> /code/.env
RUN echo "RATE_LIMIT_BURST=$RATE_LIMIT_BURST" >> /code/.env
RUN echo "UMAMI_WEBSITE_ID=$UMAMI_WEBSITE_ID" >> /code/.env

RUN pip install -U pip setuptools wheel
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt
EXPOSE 80
COPY ./app /code/app 
RUN PYTHONPATH=/code/. python /code/./app/data/scripts/get_prod_data.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
