FROM python:3.12.3
LABEL authors="MaksymStruk"

WORKDIR /backend

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/backend/app