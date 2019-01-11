FROM python:3.6

RUN apt-get update \
    && apt-get install -y \
        gdal-bin

RUN pip install uwsgi

RUN mkdir /code
WORKDIR /code
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["uwsgi", "--ini", "uwsgi.ini"]
