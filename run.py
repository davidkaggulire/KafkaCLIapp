import argparse
from chatapp import parse_args, send_messages, read_messages

if __name__ == '__main__':
    args = parse_args()
    if args['command'] == "send":
        send_messages(args)
    elif args['command'] == "receive":
        read_messages(args)
