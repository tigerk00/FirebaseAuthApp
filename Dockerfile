FROM python:3.8
LABEL maintainer="tigerk00"

ENV PYTHONUNBUFFERED 1

COPY ./django_firebase_auth /django_firebase_auth

COPY requirements.txt /django_firebase_auth/requirements.txt

WORKDIR /django_firebase_auth

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r requirements.txt

EXPOSE 8000

ENV PATH="/py/bin:$PATH"