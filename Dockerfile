# starting with ubuntu...
FROM ubuntu:16.04

# get python stuff
RUN apt-get update
RUN apt-get install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx

# now get pip
RUN pip3 install --upgrade pip
RUN pip3 install virtualenv

# clone the git repo
# RUN git clone https://github.com/Nerdenator/tagging_tracker

# make working directory
RUN mkdir /tagging_tracker

# change directory
WORKDIR /tagging_tracker

# put requirements.txt
ADD requirements.txt /tagging_tracker/

# install pip stuff
RUN pip install -r requirements.txt


ADD . /tagging_tracker/