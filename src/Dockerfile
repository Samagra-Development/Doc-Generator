# pull official base image
FROM ubuntu:20.04

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ Asia/Kolkata

# install python
RUN apt-get update -qy && apt-get install -y wget
RUN apt-get update -qy
RUN apt-get -qq -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq -y install \
    python3-dev python3-pip postgresql postgresql-contrib libffi-dev libpq-dev gcc musl-dev sudo \
    fonts-indic -o Dpkg::Progress-Fancy="1"

# install wkhtmltopdf
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
RUN apt-get -qq -y install ./wkhtmltox_0.12.6-1.focal_amd64.deb
#RUN apt-get install wkhtmltopdf

# install dependencies
#RUN pip install --upgrade pip
#RUN pip install --upgrade setuptools
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

USER root
# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
