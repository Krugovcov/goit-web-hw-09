import json
from datetime import datetime
from faker import Faker
import pika
import connect
from models import Contact

fake = Faker("uk_UA")

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        port=5672,
        credentials=credentials)
)
channel = connection.channel()

exchange = "Email Service"
queue_name = "email_sender"

channel.exchange_declare(exchange=exchange, exchange_type="direct")
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange, queue=queue_name)


def create_tasks(nums: int):
    for i in range(nums):
        contact = Contact(fullname=fake.full_name(), email=fake.email(), phone=fake.phone_number(), address=fake.address()).save()

        channel.basic_publish(
            exchange=exchange,
            routing_key=queue_name,
            body=str(contact.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    connection.close()


if __name__ == "__main__":
    create_tasks(1000)
