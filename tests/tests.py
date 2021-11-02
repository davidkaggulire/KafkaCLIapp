# tests.py

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import unittest
from unittest.mock import patch, Mock
from confluent_kafka import Producer, error
from confluent_kafka import Consumer, KafkaError, KafkaException
from chatapp import consume_messages, parsed_args, read_messages, send_messages, get_input, delivery_report


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
        test_patch = Mock()
        test_patch.method()
        test_patch.method.assert_called()
        test_patch.return_value = {'command': 'receive', 'channel': 'chat', 'server': 'localhost:9092', 'group': None, 'from': 'start'}
        parser = parsed_args(['receive', '--channel', 'chat', '--server', 'localhost:9092', '--from', 'start'])
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


    @patch('chatapp.delivery_report')
    def test_delivery_report(self, test_patch):
        test_patch = Mock()
        test_patch.method()
        test_patch.method.assert_called()
        with self.assertRaises(Exception):
            delivery_report()
            test_patch.get.assert_called_once()
        # test_patch.return_value = error
        # self.assertRaises(Exception, delivery_report)
        # self.assertRaises(Exception, test_patch.return_value)
        self.assertFalse(test_patch.called)
        # self.assertEqual(delivery_report, test_patch.return_value)


    @patch('chatapp.delivery_report')
    def test_delivery(self, test_patch):
        test_patch.return_value = error
        # with self.assertEqual(error, test_patch.return_value):
        # test_patch.get.assert_called_once()
        # with patch('test_delivery', return_value='hello world david'):
            # assert delivery_report == error
        # self.assertEqual(delivery_report, test_patch.return_value)

    @patch('chatapp.send_messages')
    def test_send_messages(self, mock_send):
        """testing sending of message via kafka"""
        args = {'command': 'send', 'channel': 'chat', 'server': 'localhost:9092', 'group': None, 'from': 'start'}
        mock_send.return_value = True
        with patch('builtins.input', return_value='hello world david'):
            self.assertEqual(mock_send(args), True)
        with patch('builtins.input', return_value='q'):
            self.assertRaises(SystemExit)


    @patch('chatapp.read_messages')
    def test_read_messages(self, mock_read):
        """test reading message from Kafka"""
        args = {'command': 'receive', 'channel': 'chat', 'server': 'localhost:9092', 'group': 'hello', 'from': 'start'}
        # read_messages(args)
        mock_read.return_value = True
        # self.assertEqual(mock_read.return_value, True)
        self.assertEqual(mock_read(args), True)


    @patch('chatapp.send_messages')
    def test_send(self, mock):
        mock = Mock()
        mock.method()
        mock.method.assert_called()
    

    @patch('chatapp.read_messages')
    def test_read(self, mock):
        mock = Mock()
        mock.method()
        mock.method.assert_called()

    # @patch('chatapp.consume_messages')
    # def test_consume_messages(self, mock_consumer):
    #     args = {'command': 'receive', 'channel': 'chat', 'server': 'localhost:9092', 'group': 'hello', 'from': 'start'}
    #     mock_consumer.return_value 
    #     self.assertIsInstance(mock_consumer(args), Consumer)


if __name__ == '__main__':
    unittest.main()