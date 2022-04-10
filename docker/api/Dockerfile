FROM python:3.10

COPY requirements.txt /
RUN pip install -r /requirements.txt
ENV PYTHONPATH=./retailer

COPY . /project
WORKDIR /project

EXPOSE 8080

RUN chmod +x ./docker/wait-for-it.sh

ENTRYPOINT ["bash"]
CMD ["./docker/wait-for-it.sh", "retailer_pg:5432", "--", "bash", "run_api.sh"]

