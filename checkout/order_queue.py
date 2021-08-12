import pika
import json

## queue URL
url = 'amqps://epbetoqp:ZqQk2irehMUBfa4bJrjASEFJw8F59U0W@chimpanzee.rmq.cloudamqp.com/epbetoqp'


def publish(body):
    ''' publish a message to order queue '''

    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel
    channel.basic_publish(exchange='',
                          routing_key='order_queue',
                          body=body)

    print(f" [x] Sent {body}")
    connection.close()


def consume():
    ''' consume a message from order queue '''

    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel() # start a channel

    def callback(ch, method, properties, body):
        print(" [x] Received " + str(body))

    channel.basic_consume('order_queue',
                          callback,
                          auto_ack=True)

    print(' [*] Waiting for messages:')
    channel.start_consuming()
    connection.close()
