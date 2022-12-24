<p align="center">

<h1>Doc Generator</h1>

</p>

[![Build](https://github.com/Samagra-Development/PDF-Package/actions/workflows/docker-push.yml/badge.svg)](https://github.com/Samagra-Development/PDF-Package/actions/workflows/docker-push.yml)

## Try it :eyes:
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Samagra-Development/Doc-Generator)

## About :open_book:

An easily integrable and resusable tool built on OSS, can be easily leveraged to generate single and bulk documents in the any available formats interoperably and at same time it can upload the docs to your CDN and generate a short url for the content, you can integerate any url shortener service like bit.ly, tinyurl, etc (check our own url shortener service [here](https://github.com/Samagra-Development/yaus)). This service is developed on a plugin based model to ensure API federation across service and allow easy development of new plugins with less chances of error.

## Features :dart:

- [x] Allow doc generation(.pdf, .docx, .png) from Google Doc templates

- [x] Allow bulk request processing

- [x] Allow easy integration for multiple CDN providers

- [x] Allow easy integrations for URL shortener services

- [x] Allow real time transforms on the raw data for complex template processing

- [x] Allow audit logs for tracking doc generation stages (useful in case of tracking async requests like bulk processing requests)

- [ ] Allow image in template processing request (by url and meta)

- [ ] Interactive UI for template validation and doc preview before generation

## Requirements :scroll:

1. Your machine should have [Python](https://www.python.org/downloads/) and ```pip``` installed.

*Note: Preferable Python version (3.9.7) and Ubuntu OS version(18.04)**

2. Check the python and ubuntu version by running following commands.

```sh
python --version

lsb_release -a

```
## PRD:
[Link](https://docs.google.com/document/d/1aX9OL_LKnkAojXyfvYLjSxXoUnhlYMjVkO9Obr0Fh0E/edit?usp=sharing)

## Installation Steps :walking:

### 1. Fork it :fork_and_knife:

You can get your own fork/copy of [Doc-Generator](https://github.com/Samagra-Development/Doc-Generator) by using the <kbd><b>Fork</b></kbd> button.

### 2. Clone it :busts_in_silhouette:

You need to clone (download) it to a local machine using

```sh
https://github.com/Samagra-Development/Doc-Generator.git
```

> This makes a local copy of the repository in your machine.

Once you have cloned the `Doc-Generator` repository in GitHub, move to that folder first using the change directory command.

```sh
cd Doc-Generator
```

Move to this folder for all other commands.

### 3. Set it up :arrow_up:

Run the following commands to see that _your local copy_ has a reference to _your forked remote repository_ in GitHub :octocat:

```sh
git remote -v

origin https://github.com/Your_Username/Doc-Generator.git (fetch)

origin https://github.com/Your_Username/Doc-Generator.git (push)
```

### 4. Run it :checkered_flag:

- rename `env.sample` file to `.env` and set the correct variable values

- build and run the container `docker-compose up -d`

```sh
docker-compose up -d

```

### 5. API

Start the server and go to ```http://localhost:8000/swagger/```

> Sample Postman Collection [here](https://www.postman.com/collections/906eb4679af014e264fc)

### 6. Contribution :hammer:

1. Preequisites:

* Minio (You can find how to run a minio instance on local [here](https://docs.min.io/docs/deploy-minio-on-docker-compose.html))

* Teamplater Engine (You can find fork it [here](https://github.com/Samarth-HP/templater/tree/master) and run a docker-compose instance)

2. Update the .env file and place it in the root folder with docker-coompose file

3. Run the docker-compose file in the project root folder to run an instance of doc generator.

4. Create a superuser ```docker-compose run web python manage.py createsuperuser```

5. Got to http://localhost:8000/admin and login with your credentials

6. Create a sample GeneralConfig entry.

> Note: GeneralConfig is encrypted store for storing your configurations and credentials

Sample GeneralConfig entry:

```json
{
  "APPLICATION_SETTINGS_FILE": "gdrive_dev_settings.yaml", //needed in case of integration with google drive for docs
  "CREDENTIAL_SETTINGS_FILE": "gdrive_dev_creds.json", //needed in case of integration with google drive for docs
  "MINIO_HOST": "YOUR MINIO HOST WITH PORT", // host:port
  "MINIO_ACCESS_KEY": "", // minio/s3 username for login
  "MINIO_SECRET_KEY": "", // minio/s3 password for login
  "MINIO_BUCKET_NAME": "doc-generator", // name of the minio bucket used for storing docs
  "SHORTENER_URL": "{{yaus_host_address}}/sr/addURL" // can be any url shortener service url
}
```

> you will need to move the .yaml and .json file downloaded on first authentication with your google drive in ```creds``` folder for non interactive authentications to google drive. check this [link](https://medium.com/analytics-vidhya/how-to-connect-google-drive-to-python-using-pydrive-9681b2a14f20) for reference on how to integrate with google APIs.

>> Note: This is a sample json config which can be fetched at runtime by the service. It can store all kinds of variables in a key value pair.

7. Now you can import the postman API collections provided [above](https://www.getpostman.com/collections/9203f723b0a754454fd5) and make sample requests to check APIs.

8. You can find sample interfaces for creating new Plugin creation [here](https://github.com/Samagra-Development/Doc-Generator/tree/v2/src/pdf/base/interfaces).

You can check sample plugins [here](https://github.com/Samagra-Development/Doc-Generator/tree/v2/src/pdf/plugins).

### 7. Documentation :book:

> Docs can be found [here](https://documenter.getpostman.com/view/10166110/UyxogiW3)
