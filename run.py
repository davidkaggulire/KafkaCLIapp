import argparse
import sys
from chatapp import parsed_args, send_messages, read_messages

if __name__ == '__main__':
    args = parsed_args(sys.argv[1:])
    print(args)
    if args['command'] == "send":
        send_messages(args)
    elif args['command'] == "receive":
        read_messages(args)
