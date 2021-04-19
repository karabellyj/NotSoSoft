FROM python:3.8-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev fontconfig ttf-dejavu

RUN pip install --upgrade pip
COPY ./requirements .
RUN pip install -r production.txt

COPY . .

RUN adduser -D dockeruser
USER dockeruser
