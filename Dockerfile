FROM python:3.10
ENV UNICODE_VERSION=15.0.0
ENV ENV=PROD
ENV REDIS_URL=redis://:5d4358184e5a1efd7688d8031ae4123ffde475018d4d8a21519e38704c24c39a@dokku-redis-vig-cache:6379
WORKDIR /code
RUN pip install -U pip setuptools wheel
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 80
COPY ./app /code/app 
RUN PYTHONPATH=/code/. python /code/./app/data/scripts/get_prod_data.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
