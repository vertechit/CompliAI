FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY arquivos /code
COPY *.py /code
COPY genie /code/genie
COPY llm /code/llm
COPY models /code/models
COPY controllers /code/controllers

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
