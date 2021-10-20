""" tests.py """
import sys
import os
import unittest
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from confluent_kafka import Producer
from confluent_kafka import Consumer, KafkaError, KafkaException
from chatapp import parse_args, read_messages, send_messages



class TestScrapping(unittest.TestCase):
    def test_parser(self):
        parser = parse_args()
        




if __name__ == '__main__':
    unittest.main()