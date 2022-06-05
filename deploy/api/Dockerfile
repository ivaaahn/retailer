FROM python:3.10-slim

ENV POETRY_VERSION=1.0.0

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /project
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY ./retailer .

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait.sh
RUN chmod +x /wait.sh && chmod +x ./run.sh

ENV DEPLOY_MODE="true"
CMD /wait.sh && ./run.sh

