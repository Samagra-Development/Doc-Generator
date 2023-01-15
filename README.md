<p align="center">

<h1>Doc Generator</h1>

</p>

[![Build](https://github.com/Samagra-Development/PDF-Package/actions/workflows/docker-push.yml/badge.svg)](https://github.com/Samagra-Development/PDF-Package/actions/workflows/docker-push.yml)

## About :open_book:

An easily integrable and resusable tool built on OSS, can be easily leveraged to generate single and bulk documents in the any available formats interoperably and at same time it can upload the docs to your CDN and generate a short url for the content, you can integerate any url shortener service like bit.ly, tinyurl, etc (check our own url shortener service [here](https://github.com/Samagra-Development/yaus)). This service is developed on a plugin based model to ensure API federation across service and allow easy development of new plugins with less chances of error.

## Dev Setup
```bash

# start all microservices and application(watch mode)
$ bash run.sh start

# stop all microservices
$ bash run.sh stop

# help
$ bash run.sh --help
```

## Test

```bash
# unit tests
$ yarn run test

# e2e tests
$ yarn run test:e2e

# test coverage
$ yarn run test:cov
```
