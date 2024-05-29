FROM node:22

ENV APP_HOME=/usr/src/app
ENV APP_USER=appuser

RUN adduser --home "$APP_HOME" "$APP_USER"
USER $APP_USER
WORKDIR $APP_HOME

COPY chat/package*.json ./
COPY chat /usr/src/app

ENV WEB_BASE_URL='http://api:80'

RUN rm -rf node_modules && yarn install --ignore-scripts --frozen-lockfile && yarn cache clean --force
RUN yarn build


EXPOSE 3000

ENTRYPOINT ["node", ".output/server/index.mjs"]

