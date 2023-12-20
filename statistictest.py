import pika
import random
import json

class Producer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='statistics_queue')

    def produce_numbers(self):
        while True:
            number = random.randint(1, 100)
            message = {'number': number}
            self.channel.basic_publish(
                exchange='',
                routing_key='statistics_queue',
                body=json.dumps(message)
            )

class Consumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='statistics_queue')

    def consume_numbers(self):
        self.channel.basic_consume(queue='statistics_queue', on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        number = message['number']
        statistics_service = StatisticsService()
        statistics_service.calculate_average(number)

class StatisticsService:
    def __init__(self):
        self.total_sum = 0
        self.total_count = 0

    def calculate_average(self, number):
        self.total_sum += number
        self.total_count += 1
        average = self.total_sum / self.total_count
        print(f"Received: {number}, Current Average: {average}")



if __name__ == "__main__":
    producer = Producer()
    consumer = Consumer()

    producer.produce_numbers()
    consumer.consume_numbers()
