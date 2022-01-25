import pika

params=pika.URLParameters('amqps://oclbtaei:ufyfhTX9WVNVtlG7748JrSusGwH6EHkZ@hornet.rmq.cloudamqp.com/oclbtaei')

connection=pika.BlockingConnection(params)

channel=connection.channel()


channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('recieved in admin')
    print(body)

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('started consuming')
channel.start_consuming()
channel.close()

