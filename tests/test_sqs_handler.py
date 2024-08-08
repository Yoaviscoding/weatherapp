# import unittest
# from unittest.mock import patch
# from processor.sqs_handler import SQSHandler
#
# # Constants for AWS credentials
# TEST_AWS_ACCESS_KEY_ID = 'AKIA4P7QLXM6WCU3ZNDS'
# TEST_AWS_SECRET_ACCESS_KEY = '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'
#
# class TestSQSHandler(unittest.TestCase):
#
#     @patch('processor.sqs_handler.boto3.client')
#     def test_send_to_sqs(self, mock_boto_client):
#         mock_sqs_client = mock_boto_client.return_value
#         mock_sqs_client.send_message.return_value = {'MessageId': '12345'}
#
#         sqs_handler = SQSHandler(TEST_AWS_ACCESS_KEY_ID, TEST_AWS_SECRET_ACCESS_KEY)
#         message = {'test': 'data'}
#
#         sqs_handler.send_to_sqs(message)
#         mock_sqs_client.send_message.assert_called_once_with(
#             QueueUrl='https://sqs.us-east-1.amazonaws.com/858960673597/exercise-exodus',
#             MessageBody='{"test": "data"}'
#         )
#
#     @patch('sqs_handler.boto3.client')
#     def test_fetch_message(self, mock_boto_client):
#         mock_sqs_client = mock_boto_client.return_value
#         mock_sqs_client.receive_message.return_value = {
#             'Messages': [{
#                 'Body': '{"test": "data"}',
#                 'ReceiptHandle': 'SomeReceiptHandle'
#             }]
#         }
#
#         sqs_handler = SQSHandler(TEST_AWS_ACCESS_KEY_ID, TEST_AWS_SECRET_ACCESS_KEY)
#         message = sqs_handler.fetch_message()
#         self.assertIsNotNone(message)
#         self.assertEqual(message['Body'], '{"test": "data"}')
#
#     @patch('sqs_handler.boto3.client')
#     def test_delete_message(self, mock_boto_client):
#         mock_sqs_client = mock_boto_client.return_value
#
#         sqs_handler = SQSHandler(TEST_AWS_ACCESS_KEY_ID, TEST_AWS_SECRET_ACCESS_KEY)
#         sqs_handler.delete_message('SomeReceiptHandle')
#         mock_sqs_client.delete_message.assert_called_once_with(
#             QueueUrl='https://sqs.us-east-1.amazonaws.com/858960673597/exercise-exodus',
#             ReceiptHandle='SomeReceiptHandle'
#         )
#
# if __name__ == '__main__':
#     unittest.main()