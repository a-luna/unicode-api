FROM python:3.11

ENV ENV=PROD
ARG ARG_UNICODE_VERSION
ENV UNICODE_VERSION=${ARG_UNICODE_VERSION}

WORKDIR /code
RUN pip install -U pip setuptools wheel
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 80
COPY ./app /code/app 
RUN PYTHONPATH=/code/. python /code/./app/data/scripts/get_prod_data.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
