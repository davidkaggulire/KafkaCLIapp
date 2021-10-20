from confluent_kafka import Producer
from confluent_kafka import Consumer, KafkaError, KafkaException
import argparse
import sys


def parse_args():
    """
    parse command line arguments needed for Kafka
    """
    parser = argparse.ArgumentParser(description="Send and receive messages using Kafka CLI")
    parser.add_argument('command', choices=['send', 'receive'], help="Parse in either send or receive")
    parser.add_argument('--channel', required=True, help="the channel or topic to send the message to")
    parser.add_argument('--server', required=True, help="server connection")
    parser.add_argument('--group', help="group to send messages to")
    parser.add_argument('--from', choices=['start', 'latest'], default='start', help="choose which messages by start or latest")
    args = parser.parse_args()
    return vars(args)


def send_messages(args):
    """
    function to send messages
    """
    connection = args['server']
    print(f"{connection} is the connection")
    p = Producer({'bootstrap.servers': connection})

    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
    
    data = input("Enter message to send or 'q' to quit: ")

    if data == 'q':
        sys.exit(0)

    p.produce('chat', data.encode('utf-8'), callback=delivery_report)
    p.flush()
    return True

def read_messages(args):
    """
    function to read messages
    """
    message_level = {
        'start': 'earliest',
        'latest': 'latest'
    }
    c = Consumer({
        'bootstrap.servers': args['server'],
        'group.id': 'mygroup',
        'auto.offset.reset': message_level[args['from']]
    })
    try:
        c.subscribe([args['channel']])

        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print("Consumer error: {}".format(msg.error()))
                    continue

            print('Received message: {}'.format(msg.value().decode('utf-8')))
    except KafkaException:
        pass
    
    finally:
        c.close()
        print("success")

    return True
