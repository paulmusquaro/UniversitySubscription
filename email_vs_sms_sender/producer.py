import json
import pika
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField


connect(host="mongodb+srv://paulmusquaro:thelastjedi@cluster0.xdsjw4l.mongodb.net/", ssl=True)


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    is_sent = BooleanField(default=False)
    phone_number = StringField(required=True)
    preferred_contact_method = StringField(choices=["email", "sms"], default="email")


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    email_queue_name = 'email_contacts_queue'
    sms_queue_name = 'sms_contacts_queue'

    fake = Faker()
    num_contacts = 10

    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()
        preferred_contact_method = fake.random_element(elements=("email", "sms"))

        contact = Contact(full_name=full_name, email=email, phone_number=phone_number, preferred_contact_method=preferred_contact_method)
        contact.save()

        message_body = {
            'contact_id': str(contact.id)
        }

        if preferred_contact_method == "email":
            channel.basic_publish(
                exchange='',
                routing_key=email_queue_name,
                body=json.dumps(message_body).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                )
            )
        elif preferred_contact_method == "sms":
            channel.basic_publish(
                exchange='',
                routing_key=sms_queue_name,
                body=json.dumps(message_body).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                )
            )

        print(f"Contact added to queue: {full_name}, {email}, {phone_number}, Preferred method: {preferred_contact_method}")


if __name__ == '__main__':
    main()
