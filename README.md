# Tagging Tracker Backend Services

These are the services that are powering the [Tagging Tracker Application](https://github.com/codeforkansascity/tagging-tracker).

> NOTE: To use the existing Azure and auth0 accounts that are applied to this code, you need to contact one of the developers on the team. Otherwise, you'll need to setup your own Azure account and auth0 instance to run this code.

## Getting Started

In order to checkout the code, and run it locally, the following steps are needed.

1. Install [`docker`](https://docs.docker.com/install/#support) and [`docker-compose`](https://docs.docker.com/compose/install/)

1. Checkout the repository

   ```
   git clone http://www.github.com/codeforkansascity/tagging_tracker_backend
   ```

1. Create a local.env file in the project directory. It should contain the following variables

   ```
   DEBUG - Whether the application is in debug mode. Defaults to 0 (False), set to 1 (True).
   SECRET_KEY - The secret key of the application. You can generate one here. https://www.miniwebtool.com/django-secret-key-generator/
   DEPLOYED_URL - The URL of where the application is hosted at. This isn't need if you are running locally on your device.
   LOADBALANCER_URL - The URL of the loadbalancer for the application. This isn't needed if you are running locally on your device.
   DB_NAME - Name of the database. See below for running it locally.
   DB_USER - Name of the database user. See below for running it locally.
   DB_HOST - Host of the database. See below for running it locally.
   DB_PORT - Database port. See below for running it locally.
   DB_PASSWORD - Database Password. See below for running it locally.
   SSL_MODE - The SSL mode of the database connection. Defaults to disable.
   SSL_ROOT_CERT - The path of the SSL certificate. Defaults to empty string, and not used if SSL is disabled.
   AUTH0_URL - URL of the auth0 authentication engine.
   AUTH0_CLIENTID - ClientID of the auth0 authentication engine.
   AUTH0_SECRET - Secret of the auth0 authentication engine.
   LOG_LEVEL - Error/Reporting logging level. More information here https://docs.djangoproject.com/en/2.0/topics/logging/#configuring-logging
   AZURE_IMAGE_CONTAINER_NAME - Azure container name for file uploads.
   AZURE_IMAGE_CONTAINER_KEY - Azure container access key.
   ```

   To get you started and running locally, here is a local.env file you can use.

   ```
   DEBUG=1
   SECRET_KEY=<Your generated key>
   DB_NAME=dev
   DB_USER=tag_user
   DB_PASSWORD=somepass
   AUTH0_URL=<Create your own auth0 or ask developers for it>
   AUTH0_CLIENTID=<Create your own auth0 or ask developers for it>
   AUTH0_SECRET=<Create your own auth0 or ask developers for it>
   SSL_MODE=disable
   LOG_LEVEL=DEBUG
   AZURE_IMAGE_CONTAINER_NAME=taggingtrackerdevimages
   AZURE_IMAGE_CONTAINER_KEY=<Attend meetup to obtain>
   ```

There are 2 methods of running the development environment. First is via a [virtualenv](#virtualenv-instructions) with a postgres `docker` image.
Secondly you can use [docker-compose](#docker-compose-instructions).

## Virtualenv instructions

These instructions assume you already have a virtualenv setup with a python 3.6 distribution.

1. Run the following commands

```bash
# Install all the requirements
$ make reqs
# Start development server
$ make start
# After exiting dev server process stop and remvoe all containers
$ make stop
```


## Docker compose instructions

1. Run the following commands

   ```bash
   # build and runs all containers
   $ make && make up
   # in a seperate terminal
   $ make migratelocal
   # or run in detached mode
   $ make && make upd && make migratelocal
   ```

   Anytime you change application code run `make reload` to restart `uwsgi` in the container.

   When finished run `make down` to stop all services. There are other targets available in the [Makefile](Makefile) that also help
   with development so feel free to look those over.

1. (Optional) Configure your own settings by creating a
  [docker-compose.override.yml](https://docs.docker.com/compose/extends/#understanding-multiple-compose-files)
  file. See
  [Docker Compose](https://docs.docker.com/compose/compose-file/) for a list
  of additional settings.

   > NOTE: To configure ports properly, `docker-compose.override.yml` must
 contain all settings from the `docker-compose.yml`.
 [Refer to this](https://stackoverflow.com/a/48863743) for more details. To
  run, use `docker-compose -f docker-compose.override.yml up`

1. (Optional) Generate your own self signed certificate pointing to the localhost domain using `make ssl`.

# Managing requirements

We use [`pip-tools`](https://github.com/jazzband/pip-tools) to manage our requirements. High level application packages should be
put in `requirements.in` and high level development/testing packages should be put in `requirements-dev.in`. Once there run
`make compile` to generate new requirements files and then `make reqs` to install the updates.

# Contribution

Read the [Contribution Guide](docs/CONTRIBUTING.md)
