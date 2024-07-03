FROM python:3.12-slim as base
LABEL maintainer="Konstantin Osipov <kosipov@list.ru>"


WORKDIR /opt/earthquake

COPY . .

RUN pip3 install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENTRYPOINT ["./entrypoint.sh"]