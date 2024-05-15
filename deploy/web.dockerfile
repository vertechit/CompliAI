FROM node:latest
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY chat/package*.json ./
COPY chat /usr/src/app

ENV WEB_BASE_URL='http://api:80'

RUN rm -rf node_modules && yarn install --ignore-scripts --frozen-lockfile && yarn cache clean --force
RUN yarn build


EXPOSE 3000

ENTRYPOINT ["node", ".output/server/index.mjs"]

