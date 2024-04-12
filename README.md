# UniversityUtilities

## 1. Storage of Quotes

This project is a quotes repository. It uses Mongoengine and Redis. The system allows you to find quotes by author name or tags.

##### System Components

- `models.py`: Defines the Author and Quote document schemas for Mongoengine.
- `seeds`: Uploads data into the database.
- `main.py`: Script to find the quotes you want.

## 2. Email/SMS Sender

This project demonstrates a simple notification system that utilizes RabbitMQ for message queuing and Mongoengine for object-document mapping to MongoDB. The system simulates sending email and SMS notifications to contacts stored in a database.

##### System Components

- `producer.py`: Script that generates fake contact data and queues messages in RabbitMQ for sending notifications.
- `consumer_email.py`: Script that listens for email notification requests and processes them.
- `consumer_sms.py`: Script that listens for SMS notification requests and processes them.

## Requirements

- Python 3
- RabbitMQ
- MongoDB
- Pika (RabbitMQ Python client)
- Mongoengine
- Faker (for generating fake data)
- Redis