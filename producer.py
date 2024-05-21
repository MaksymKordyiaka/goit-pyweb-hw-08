import pika
from faker import Faker
from mongoengine import connect
from models import Contact

fake = Faker()

# Підключення до MongoDB
connect("contacts_db", host="localhost", port=27017)

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

# Генерування фейкових контактів та їх збереження в базу даних
def generate_contacts(num_contacts):
    for _ in range(num_contacts):
        fullname = fake.name()
        email = fake.email()
        contact = Contact(fullname=fullname, email=email)
        contact.save()
        # Поміщення ObjectID створеного контакту у чергу RabbitMQ
        channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))

generate_contacts(10)  # Генеруємо 10 контактів
print("Generated and sent 10 contacts to the email queue")

connection.close()
