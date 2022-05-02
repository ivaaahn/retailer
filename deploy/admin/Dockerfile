FROM python:3.10-slim

WORKDIR /project

COPY requirements_admin.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./retailer_admin .
COPY ./deploy/wait-for-it.sh wait.sh

RUN chmod +x wait.sh

ENTRYPOINT ["bash"]
CMD ["./wait.sh", "app:8080", "-t", "45", "--", "bash", "./run.sh"]

