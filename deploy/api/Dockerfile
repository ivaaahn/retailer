FROM python:3.10-slim

WORKDIR /project

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./retailer .

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait.sh
RUN chmod +x /wait.sh && chmod +x ./run.sh

ENV DEPLOY_MODE="true"
CMD /wait.sh && ./run.sh

