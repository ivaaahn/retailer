FROM python:3.10-slim

WORKDIR /project

COPY requirements_admin.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./retailer_admin .

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait.sh
RUN chmod +x /wait.sh
RUN chmod +x ./run.sh

CMD /wait.sh && ./run.sh
