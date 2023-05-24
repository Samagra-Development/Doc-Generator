FROM node:16

WORKDIR /app

COPY . .

RUN yarn install

RUN npx prisma generate

RUN yarn run build

CMD ["yarn", "start:prod"]
