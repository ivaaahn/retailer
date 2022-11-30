FROM rabbitmq:3-management-alpine

COPY etc/definitions.json rabbitmq.conf /etc/rabbitmq/
RUN chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq.conf /etc/rabbitmq/definitions.json
