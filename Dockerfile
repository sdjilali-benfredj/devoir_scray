FROM mongo:latest

RUN apt-get update && \
    apt-get install -y python3 python3-pip

COPY requirements.txt /usr/src/app/
RUN pip3 install -r /usr/src/app/requirements.txt

COPY . /usr/src/app

WORKDIR /usr/src/app

EXPOSE 5000

CMD mongod --fork --logpath /var/log/mongod.log && python3 app.py