FROM rabbitmq:3.12.9-management

COPY ./conf/enabled_plugins /etc/rabbitmq/enabled_plugins
COPY ./conf/rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

EXPOSE 15672
EXPOSE 5672
EXPOSE 1883
