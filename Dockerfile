# starting with ubuntu...
FROM ubuntu:16.04

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl

# get python stuff
RUN apt-get update
RUN apt-get install -y software-properties-common python-software-properties dialog apt-utils wget
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt xenial-pgdg main" >> /etc/apt/sources.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update
RUN apt-get install -y python3-pip python3-dev libpq-dev nginx
RUN apt-get install -y postgresql-9.6
RUN apt-get install -y postgresql-9.6-postgis-2.3 postgresql-contrib-9.6 postgis postgresql-9.6-postgis-2.3-scripts

# now get pip
RUN pip3 install --upgrade pip
RUN pip3 install virtualenv

# make working directory
RUN mkdir /code

# change directory
WORKDIR /code

# put requirements.txt
ADD requirements.txt /code/

# install pip stuff
RUN pip install -r requirements.txt

ADD . /code/

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
