FROM node:latest
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package*.json ./
COPY . .

ENV WEB_BASE_URL='http://api:80'

RUN rm -rf node_modules && yarn install --frozen-lockfile && yarn cache clean --force
RUN yarn build


EXPOSE 3000

ENTRYPOINT ["node", ".output/server/index.mjs"]

