FROM python:3.10.5
WORKDIR /code
RUN pip install -U pip setuptools wheel
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
EXPOSE 80
COPY ./app /code/app 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
