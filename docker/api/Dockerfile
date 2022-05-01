FROM python:3.10-slim

WORKDIR /project

COPY requirements_app.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./retailer .
COPY ./docker/wait-for-it.sh wait.sh

RUN chmod +x wait.sh

ENTRYPOINT ["bash"]
CMD ["./wait.sh", "pg:5432", "-t", "30", "--", "bash", "./run.sh"]

