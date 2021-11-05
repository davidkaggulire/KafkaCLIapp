# tests.py

import sys
import os
from typing import Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import unittest
from unittest.mock import patch, Mock, create_autospec
from confluent_kafka import Producer, error
from confluent_kafka import Consumer, KafkaError, KafkaException
from chatapp import consume_messages, parsed_args, read_messages, send_messages, get_input, delivery_report, encode_func
from chatapp import consume_messages, encode_func, parsed_args, read_messages, send_messages, get_input, delivery_report
from unittest import mock
import chatapp


class TestChatApp(unittest.TestCase):

    def test_empty_parsed_args(self):
        """test parsed_args func with empty args"""
        with self.assertRaises(SystemExit):
            parsed_args(sys.argv[1:])


    def test_normal_parser(self):
        """testing parsing args to function"""
        parser = parsed_args(
            ['send', '--channel', 'chat', '--server', 'localhost:9092'])
        self.assertIsInstance(parser, dict)


    @patch('chatapp.parsed_args')
    def test_parser_send(self, test_patch):
        """testing parsing command send"""
        test_patch.return_value = {'command': 'send', 'channel': 'chat',
                                   'server': 'localhost:9092', 'group': None, 'from': 'start'}
        parser = parsed_args(
            ['send', '--channel', 'chat', '--server', 'localhost:9092'])
        self.assertIsInstance(parser, dict)
        self.assertEqual(parser, test_patch.return_value)


    @patch('chatapp.parsed_args')
    def test_parser_receive(self, test_patch):
        """testing parsing command receive"""
        test_patch.return_value = {'command': 'receive', 'channel': 'chat',
                                   'server': 'localhost:9092', 'group': None, 'from': 'start'}
        parser = parsed_args(['receive', '--channel', 'chat',
                             '--server', 'localhost:9092', '--from', 'start'])
        self.assertIsInstance(test_patch.return_value, dict)
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


    @patch('chatapp.send_messages')
    @patch('chatapp.encode_func')
    @patch('chatapp.delivery_report')
    def test_send_messages(self, mock_send, mock_encode, mock_delivery):
        """testing sending of message via kafka"""
        args = {'command': 'send', 'channel': 'chat',
                'server': 'localhost:9092', 'group': "hello", 'from': 'start'}
        
        mock_encode.return_value = b'some content you want to decode'
        mock_send.return_value = True

        with patch('builtins.input', return_value=b'some content you want to decode'):
            result = send_messages(args)
            assert mock_encode.called is True

            self.assertEqual(result, mock_send())
        with patch('builtins.input', return_value='q'):
            self.assertRaises(SystemExit)


    @patch('chatapp.read_messages')
    def test_read_messages(self, mock_read):
        """test reading message from Kafka"""
        args = {'command': 'receive', 'channel': 'chat',
                'server': 'localhost:9092', 'group': 'hello', 'from': 'start'}
        read_messages(args)
        mock_read.return_value = True
        self.assertEqual(mock_read.return_value, True)


    @patch('chatapp.consume_messages')
    def test_consume_messages(self, mock_consumer):
        args = {'command': 'receive', 'channel': 'chat',
                'server': 'localhost:9092', 'group': 'hello', 'from': 'start'}
        arg2 = {
            'bootstrap.servers': args['server'],
            'group.id': args['group'],
            'auto.offset.reset': 'beginning'
        }
        mock_consumer.return_value = Consumer(arg2)

        result = consume_messages(args)

        self.assertIsInstance(mock_consumer.return_value, Consumer)
        self.assertIsInstance(result, Consumer)

    @patch('chatapp.encode_func')
    def test_encode_func(self, mock_sample_fct):
        mock_sample_fct.return_value = mock.Mock(
            content=b'some content you want to decode')
        with patch('builtins.input', return_value='some content you want to decode'):
            result = encode_func(get_input)
            self.assertEqual(b'some content you want to decode', result)

    @patch('chatapp.delivery_report')
    def test_delivery_report_error(self, mock_delivery):
        mock_delivery.return_value = mock.Mock("Message delivery failed: err")
        result = delivery_report("err", "msg")
        self.assertEqual("Message delivery failed: err", result)
        self.assertFalse(mock_delivery.called)


if __name__ == '__main__':
    unittest.main()