# opening-hours

### [Notes for the reviewer](notes.md)

## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).

## Backend local development

### The .env file

First, create a `.env` file and put it inside the root folder of the project.  
The `.env` file is the one that contains all your configurations.
You can copy/paste the contents from `.env.example` to your `.env` file.


### Running
* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* Now you can open your browser and interact with these URLs:

Backend, JSON based web API based on OpenAPI

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

<img src="images/swagger.png" width="755" height="422">

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

<img src="images/redoc.png" width="755" height="422">

Traefik UI, to see how the routes are being handled by the proxy: http://localhost:8090

<img src="images/traefik.png" width="755" height="422">

**Note**: The first time you start your stack, it might take a few minutes for it to be ready. While the backend configures everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker-compose logs
```

## Backend local development, additional details

### General workflow

Modify or add Pydantic schemas in `./backend/app/app/schemas/`, API endpoints in `./backend/app/app/api/`, API helpers or utils in `./backend/app/app/api/helpers`. 

### Docker Compose Override

During development, you can change Docker Compose settings that will only affect the local development environment, in the file `docker-compose.override.yml`.

The changes to that file only affect the local development environment, not the production environment. So, you can add "temporary" changes that help the development workflow.

### Backend tests

To test the backend run:

```console
$ DOMAIN=backend sh ./scripts/test.sh
```

The file `./scripts/test.sh` has the commands to generate a testing `docker-stack.yml` file, start the stack and test it.

To run the tests in a running stack:

```bash
docker-compose exec backend bash /app/tests-start.sh
```
<img src="images/tests.png" width="755" height="422">

The tests run with Pytest, modify and add tests to `./backend/app/app/tests/`.

### Backend tests, additional details

If you need to pass extra arguments to `pytest`, you can pass them to this command and they will be forwarded.
For example, to stop on first error:

```bash
docker-compose exec backend bash /app/tests-start.sh -x
```

If you use GitLab CI the tests will automatically run.

## Deployment

You can deploy the stack to a Docker Swarm mode cluster with a main Traefik proxy, set up using the ideas from <a href="https://dockerswarm.rocks" target="_blank">DockerSwarm.rocks</a>, to get automatic HTTPS certificates, etc.

And you can use CI (continuous integration) systems to do it automatically.

But you have to configure a couple of things first.

### Traefik network

This stack expects the public Traefik network to be named `traefik-public`, just as in the tutorials in <a href="https://dockerswarm.rocks" class="external-link" target="_blank">DockerSwarm.rocks</a>.

If you need to use a different Traefik public network name, update it in the `docker-compose.yml` files, in the section:

```YAML
networks:
  traefik-public:
    external: true
```

Change `traefik-public` to the name of the used Traefik network. And then update it in the file `.env`:

```bash
TRAEFIK_PUBLIC_NETWORK=traefik-public
```

**Note**: The `${STACK_NAME?Variable not set}` means "use the environment variable `STACK_NAME`, but if it is not set, show an error `Variable not set`".

### Deploy to a Docker Swarm mode cluster

There are 3 steps:

1. **Build** your app images
2. Optionally, **push** your custom images to a Docker Registry
3. **Deploy** your stack

---

Here are the steps in detail:

1. **Build your app images**

* Set these environment variables, right before the next command:
  * `TAG=prod`
* Use the provided `scripts/build.sh` file with those environment variables:

```bash
TAG=prod bash ./scripts/build.sh
```

2. **Optionally, push your images to a Docker Registry**

**Note**: if the deployment Docker Swarm mode "cluster" has more than one server, you will have to push the images to a registry or build the images in each server, so that when each of the servers in your cluster tries to start the containers it can get the Docker images for them, pulling them from a Docker Registry or because it has them already built locally.

If you are using a registry and pushing your images, you can omit running the previous script and instead using this one, in a single shot.

* Set these environment variables:
  * `TAG=prod`
* Use the provided `scripts/build-push.sh` file with those environment variables:

```bash
TAG=prod bash ./scripts/build-push.sh
```

3. **Deploy your stack**

* Set these environment variables:
  * `DOMAIN=opening-hour.com`
  * `TRAEFIK_TAG=opening-hour.com`
  * `STACK_NAME=opening-hour-com`
  * `TAG=prod`
* Use the provided `scripts/deploy.sh` file with those environment variables:

```bash
DOMAIN=opening-hour.com \
TRAEFIK_TAG=opening-hour.com \
STACK_NAME=opening-hour-com \
TAG=prod \
bash ./scripts/deploy.sh
```

---

### Continuous Integration / Continuous Delivery

If you use GitLab CI, the included `.gitlab-ci.yml` can automatically deploy it. You may need to update it according to your GitLab configurations.

GitLab CI is configured assuming 2 environments following GitLab flow:

* `prod` (production) from the `production` branch.
* `stage` (staging) from the `master` branch.
