FROM python:3.9

RUN apt-get update

RUN pip install --upgrade pip

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

ENTRYPOINT ["bash", "/app/entrypoint.sh"]

