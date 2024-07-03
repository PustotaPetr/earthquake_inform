FROM rabbitmq:3.13.3-management

RUN apt-get update && apt-get install -y curl