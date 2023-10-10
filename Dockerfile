FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV VERSION="latest"
ENV ENVIRONMENT="dev"
ENV PROJECT="marketplace"

WORKDIR /app

COPY requirements.txt .

WORKDIR /code

COPY . ./
RUN apt-get update
RUN apt-get install sudo -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "marketplace.wsgi:application"]
