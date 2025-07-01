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

A: 1 sender and 1 consumer (just sends/consumes 1 message): sender.py & receiver.py

B: 1 consumer always listening: message_consumer.py

C: 1 sender, you can configure it to send as many messages as you want: load_test.py


### Using the HELM chart:

1. Navigate to the directory containing the chart: 
```
cd helm
```

2. Install the Helm chart into your local Kubernetes cluster:
```
helm install rabbitmq . --namespace default
```

3. Verify the deployment:
```
kubectl get pods,svc
```

4. Access the RabbitMQ management console by enabling port forwarding and navigating to: 
```
kubectl port-forward svc/rabbitmq 15672:15672
```

5. Access the AMQP Port by enabling port forwarding:
```
kubectl port-forward svc/rabbitmq 5672:5672
```

