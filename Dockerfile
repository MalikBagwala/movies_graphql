FROM python:3.6-slim
LABEL maintainer="m.bagwala@gmail.com"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8081
COPY . .