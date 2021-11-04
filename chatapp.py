# chatapp.py

from confluent_kafka import Producer, Consumer, KafkaError
import argparse
import sys


def parsed_args(args):
    """
    parse command line arguments needed for Kafka
    """
    parser = argparse.ArgumentParser(description="Send and receive messages using Kafka CLI")
    parser.add_argument('command', choices=['send', 'receive'], help="Parse in either send or receive")
    parser.add_argument('--channel', required=True, help="the channel or topic to send the message to")
    parser.add_argument('--server', required=True, help="server connection")
    parser.add_argument('--group', help="group to send messages to")
    parser.add_argument('--from', choices=['start', 'latest'], default='start', help="choose which messages by start or latest")
    args = parser.parse_args(args)
    return vars(args)


def get_input():
    data = input("Enter message to send or 'q' to quit: ")
    if data == 'q':
        sys.exit(0)
    return data


def encode_func(func):
    returned_data = func()
    return returned_data.encode('utf-8')


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err:
        return 'Message delivery failed: {}'.format(err)
    else:
        return 'Message delivered to {} [{}]'.format(msg.topic(), msg.partition())


def send_messages(args):
    """
    function to send messages
    """
    connection = args['server']
    channel = args['channel']
    group = args['group']

    print(f"You have decided to send to the channel: {channel}")
    print(f"You are sending through the server: {connection}")
    print(f"You are sending through the group: {group}")

    p = Producer({'bootstrap.servers': connection})    
    
    data = encode_func(get_input)
    
    p.produce(channel, data, callback=delivery_report)
    p.flush()
    return True


def consume_messages(args):
    """
    function to read messages
    """
    channel = args['channel']
    server = args['server']
    start_from = args['from']
    group = args['group']

    print(f"You are receiving from the channel: {channel}")
    print(f"You are receiving from the {start_from}")
    print(f"You are receiving through the server {server}")
    print(f"You are part of the receiving group: {group}")
    
    message_level = {
        'start': 'beginning',
        'latest': 'latest'
    }
    c = Consumer({
        'bootstrap.servers': args['server'],
        'group.id': args['group'],
        'auto.offset.reset': message_level[args['from']]
    })

    return c


def read_messages(args):
    c = consume_messages(args)
    c.subscribe([args['channel']])
    try:  
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print('Received message: {}'.format(msg.value().decode('utf-8')))
    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')
    
    finally:
        c.close()
        print("success")

    return True
