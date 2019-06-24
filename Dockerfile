FROM python:3.6-alpine

RUN apk update

RUN apk add \
  --no-cache \
  --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
  --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
  gdal \
  py-gdal \
  gcc \
  musl-dev \
  libffi-dev \
  postgresql-dev \
  python3-dev \
  build-base \
  linux-headers \
  pcre-dev \
  gdal-dev \
  geos-dev

RUN pip install --no-cache-dir uwsgi

RUN mkdir /code
WORKDIR /code
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uwsgi", "--ini", "uwsgi.ini"]
