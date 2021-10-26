# tests.py

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import unittest
from unittest.mock import patch
from confluent_kafka import Producer
from confluent_kafka import Consumer, KafkaError, KafkaException
from chatapp import parsed_args, read_messages, send_messages, get_input, delivery_report


class TestChatApp(unittest.TestCase):

    def test_empty_parsed_args(self):
        """test parsed_args func with empty args"""
        with self.assertRaises(SystemExit):
            parsed_args(sys.argv[1:])

    
    def test_normal_parser(self):
        """testing parsing args to function"""
        parser = parsed_args(['send', '--channel', 'chat', '--server', 'localhost:9092'])
        self.assertIsInstance(parser, dict)

    
    @patch('chatapp.parsed_args')
    def test_parser_send(self, test_patch):
        """testing parsing command send"""
        test_patch.return_value = {'command': 'send', 'channel': 'chat', 'server': 'localhost:9092', 'group': None, 'from': 'start'}
        parser = parsed_args(['send', '--channel', 'chat', '--server', 'localhost:9092'])
        self.assertIsInstance(parser, dict)
        self.assertEqual(parser, test_patch.return_value)

    
    @patch('chatapp.parsed_args')
    def test_parser_receive(self, test_patch):
        """testing parsing command receive"""
        test_patch.return_value = {'command': 'receive', 'channel': 'chat', 'server': 'localhost:9092', 'group': None, 'from': 'start'}
        parser = parsed_args(['receive', '--channel', 'chat', '--server', 'localhost:9092', '--from', 'start'])
        self.assertIsInstance(parser, dict)
        self.assertEqual(parser, test_patch.return_value)


    def test_get_input_func(self):
        """test get_input function"""
        with patch('builtins.input', return_value='y'):
            assert get_input() == 'y'
        with patch('builtins.input', return_value='q'):
            self.assertRaises(SystemExit)
        with self.assertRaises(SystemExit) as cm:
            with patch('builtins.input', return_value='q'):
                get_input()
        self.assertEqual(cm.exception.code, 0)

    
    # def test_delivery_report(self):
    #     self.assertRaises(Exception, delivery_report)


    def test_send_messages(self):
        """testing sending of message via kafka"""
        args = {'command': 'send', 'channel': 'chat', 'server': 'localhost:9092', 'group': None, 'from': 'start'}

        with patch('builtins.input', return_value='hello world david'):
            self.assertEqual(send_messages(args), True)
        with patch('builtins.input', return_value='q'):
            self.assertRaises(SystemExit)


    def test_read_messages(self):
        """test reading message from Kafka"""
        args = {'command': 'receive', 'channel': 'chat', 'server': 'localhost:9092', 'group': 'hello', 'from': 'start'}
        self.assertEqual(read_messages(args), True)


if __name__ == '__main__':
    unittest.main()