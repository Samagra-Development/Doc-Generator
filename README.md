
## About

An easily integrable and resusable tool built on OSS, can be easily leveraged to generate single and bulk documents in the any available formats interoperably.
In addition, it can
- Upload the generated docs to CDN, google drive, s3, custom sink.
- Generate a shortened URL for the uploaded file for easy sharing.

The project is built based on plugin model, to ensure customizability and wide adoption.

## C4GT 2023
- [v2](https://github.com/Samagra-Development/Doc-Generator/tree/v2) branch contains the original source code written in python, you can check it for reference.
- Join our discord here: [https://discord.com/invite/VPrXf7Jxpr](https://discord.com/invite/VPrXf7Jxpr), head to [doc-generator](https://discord.com/channels/973851473131761674/1107697276475941024) channel
- Check out [good-first-issues](https://github.com/Samagra-Development/Doc-Generator/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) to start contributing

## Running the app

```bash
# Copy env file
$ cp .env.copy .env
```

```bash
# Specify the local compose file
$ docker-compose -f docker-compose.local.yml up -d --build

# For production
$ docker-compose up -d --build
```

Check if all the containers are running using `docker ps`

## Test

```bash
# unit tests
$ yarn run test

# e2e tests
$ yarn run test:e2e

# test coverage
$ yarn run test:cov
```
