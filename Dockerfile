FROM node:16 AS builder

# Create app directory
WORKDIR /app

#RUN cp .env .env
RUN mkdir -p broker
RUN mkdir -p redisinsight
RUN chown -R 1001:1001 broker
RUN chown -R 1001:1001 redisinsight

COPY package.json ./
COPY yarn.lock ./

# Install app dependencies
RUN yarn install

COPY . .

# Generate build
RUN yarn run build

CMD [ "npx", "nx", "serve", "api" ]
