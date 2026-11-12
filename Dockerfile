FROM python:3.11.4-slim-bookworm

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./backend/requirements.txt .
RUN pip install -r requirements.txt

COPY . .