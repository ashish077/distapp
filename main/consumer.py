import json
from main import Product, db
import pika

params=pika.URLParameters('amqps://oclbtaei:ufyfhTX9WVNVtlG7748JrSusGwH6EHkZ@hornet.rmq.cloudamqp.com/oclbtaei')

connection=pika.BlockingConnection(params)

channel=connection.channel()


channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('recieved in main')
    data=json.loads(body)    
    print(body)

    if properties.content_type=='product-created':
        product=Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
    
    elif properties.content_type=='product-updated':
        product=Product.query.get(data['id'])
        product.title=data['title']
        product.image=data['image']
        db.session.commit()
    
    elif properties.content_type=='product-deleted':
        product=Product.query.get(data)
        db.session.delete(product)
        db.session.commit()



channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('started consuming')
channel.start_consuming()
channel.close()

