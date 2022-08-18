FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./models_store /code/models_store
COPY ./datasets /code/datasets

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]