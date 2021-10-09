FROM python:3.8-alpine

LABEL mantainer="Dimas Adrian Mukti <dadrianm25@gmail.com>"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN env/bin/pip install -r requirements.txt

COPY . .

ENTRYPOINT ["env/bin/python", "web_service.py"]