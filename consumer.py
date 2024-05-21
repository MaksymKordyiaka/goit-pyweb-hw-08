import pika
from time import sleep
from mongoengine import connect
from models import Contact

# Підключення до MongoDB
connect("contacts_db", host="localhost", port=27017)

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

# Функція-заглушка для імітації відправлення email
def send_email(contact_id):
    print(f"Sending email to contact with ID: {contact_id}")
    sleep(1)

# Обробник повідомлень з черги RabbitMQ
def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects.get(id=contact_id)
    if contact:
        send_email(contact_id)
        contact.email_sent = True
        contact.save()

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()



# Підписка на отримання повідомлень
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
