# RabbitMQ Load testing with Python
## Steve A.

# For local testing, you can deploy a container with a simple user/pass:

## RabbitMQ Docker image & deployment

`docker pull rabbitmq:management`

```
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=bitnami rabbitmq:management
```

### Access the RabbitMQ Management Console:
Once the container is running, you can access the RabbitMQ management console by opening a web browser and navigating to http://localhost:15672.

Use the username: **user** and password: **bitnami** to log in.

## Running the load tests:

### Python Setup:

- `python -m venv .venv`
- `source .venv/bin/activate`
- `pip3 install -r requirements.txt`
  
### Run the scripts

#### async_load_test_x_value.py

  This will write and read 10,000 messages in multi-threading mode.

- If you used the script above to deploy the container, no changes are required.
- If your rabbitmq server is different, change the username, password, and host/port values.
- Run the test: `python async_load_test_x_value.py`


### Other script scenarios:

1. You can spin up 2 scripts at once, a 