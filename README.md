
## About
The Doc-Generator is an easily integrable and reusable tool built on open-source software (OSS). It provides seamless generation of single and bulk documents in various available formats, ensuring interoperability. Additionally, it offers the following features:

- Upload the generated documents to CDN, Google Drive, S3, or a custom sink.
- Generate a shortened URL for the uploaded file for easy file sharing.

The project is built on a plugin model, which ensures customizability and wide adoption.

## C4GT 2023
- The [v2](https://github.com/Samagra-Development/Doc-Generator/tree/v2) branch contains the original source code written in python. You can refer to it for more details.
- Join our discord community here: [https://discord.com/invite/VPrXf7Jxpr](https://discord.com/invite/VPrXf7Jxpr), head to [doc-generator](https://discord.com/channels/973851473131761674/1107697276475941024) channel.
- To start contributing, check out the [good-first-issues](https://github.com/Samagra-Development/Doc-Generator/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) section.

## Installation

```bash
$ yarn install
```

## Running the app

```bash
# Run in development mode
$ yarn run start

# Run in watch mode
$ yarn run start:dev

# Run in production mode
$ yarn run start:prod
```

## Test

```bash
# Run unit tests
$ yarn run test

# Run end-to-end tests
$ yarn run test:e2e

# Generate test coverage
$ yarn run test:cov
```
