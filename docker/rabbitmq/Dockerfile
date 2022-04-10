FROM rabbitmq:3-management-alpine

ADD definitions.json /etc/rabbitmq/
ADD rabbitmq.conf /etc/rabbitmq/

RUN chown rabbitmq:rabbitmq /etc/rabbitmq/rabbitmq.conf /etc/rabbitmq/definitions.json

CMD ["rabbitmq-server"]