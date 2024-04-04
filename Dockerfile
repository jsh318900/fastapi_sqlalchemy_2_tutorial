FROM python:3.11

RUN mkdir /code/
COPY ./app/ /code/app/
COPY ./requirements.txt /code/requirements.txt

WORKDIR /code/
RUN python3.11 -m pip install -r requirements.txt

CMD uvicorn app.main:app --host 0.0.0.0 --port 8080
