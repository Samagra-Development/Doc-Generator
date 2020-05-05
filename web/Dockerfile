FROM ubuntu:18.04 as base

RUN apt-get update \
    && apt-get -y upgrade
    
RUN apt-get install -y bash gcc musl-dev libffi-dev python-dev python3-dev python3-pip libssl-dev software-properties-common 

RUN apt-get install -y graphviz libgraphviz-dev graphviz-dev pkg-config

# Set an environment variable with the directory
# where we'll be running the app
#ENV APP /app
ENV LANG C.UTF-8
# Create the directory and instruct Docker to operate
# from there from now on
#RUN mkdir $APP
WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /usr/src/app/

 RUN chmod +x src/docker-entrypoint.sh
 RUN ls -la src
ENTRYPOINT ["src/docker-entrypoint.sh"]