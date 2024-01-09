FROM python:3.8-alpine

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt --no-cache-dir

CMD [ "flask", "--app", "app", "run","--host","0.0.0.0","--port","5000"]