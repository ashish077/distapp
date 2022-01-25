#amqps://oclbtaei:ufyfhTX9WVNVtlG7748JrSusGwH6EHkZ@hornet.rmq.cloudamqp.com/oclbtaei
import json
import pika

params=pika.URLParameters('amqps://oclbtaei:ufyfhTX9WVNVtlG7748JrSusGwH6EHkZ@hornet.rmq.cloudamqp.com/oclbtaei')

connection=pika.BlockingConnection(params)

channel=connection.channel()

def publish(method, body):
    properties= pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties= properties)

