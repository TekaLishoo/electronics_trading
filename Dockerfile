FROM python:3.10 as base

ENV PYTHONUNBUFFERED=1

RUN pip install pipenv

WORKDIR /electronics_trading/

COPY . ./

RUN pipenv install --system --deploy