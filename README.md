## About

The Doc-Generator is an easily integrable and reusable tool built on open-source software (OSS). It provides seamless generation of single and bulk documents in various available formats, ensuring interoperability. Additionally, it offers the following features:

- Upload the generated documents to CDN, Google Drive, S3, or a custom sink.
- Generate a shortened URL for the uploaded file for easy file sharing.

The project is built on a plugin model, which ensures customizability and wide adoption.

## C4GT 2023

- The [v2](https://github.com/Samagra-Development/Doc-Generator/tree/v2) branch contains the original source code written in python. You can refer to it for more details.
- Join our discord community here: [https://discord.com/invite/VPrXf7Jxpr](https://discord.com/invite/VPrXf7Jxpr), head to [doc-generator](https://discord.com/channels/973851473131761674/1107697276475941024) channel.
- To start contributing, check out the [good-first-issues](https://github.com/Samagra-Development/Doc-Generator/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) section.

## Running the app

### Development

_Prerequisites_ -

- Node 16
- Yarn 1
- Docker
- Docker Compose

```bash
# Copy env file
$ cp .env.copy .env

# Specify the local compose file
$ docker-compose -f docker-compose.local.yml up -d

# Installing app dependencies
$ yarn install

# Run Prisma migrations
$ yarn prisma migrate dev -n init

# Start in watch mode
$ yarn start:dev
```

### Production

_Prerequisites_ -

- Docker
- Docker Compose

```bash
# Edit .env file according to your production setup
$ cp .env.copy .env

# Production build includes the app service
$ docker-compose up -d --build

# go inside the container
docker-compose exec app bash

# run migration
npx prisma migrate dev

# exit out of container
exit
```

Check if all the containers are running using `docker ps`

## Test

```bash
# Run unit tests
$ yarn run test

# Run end-to-end tests
$ yarn run test:e2e

# Generate test coverage
$ yarn run test:cov
```
