FROM python:3.9-alpine

WORKDIR /flask_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pytest
RUN apk add --no-cache docker-compose

COPY app/ .

COPY tests/ app/tests/

CMD [ "python", "app.py" ]
