FROM python:3.10

ENV APP_HOME=/code
ENV APP_USER=appuser

RUN adduser --home "$APP_HOME" "$APP_USER"

USER $APP_USER

ENV PATH $APP_HOME/.local/bin:${PATH}

WORKDIR /code
COPY app/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY app /code

VOLUME [ "/data" ]

CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8080"]
