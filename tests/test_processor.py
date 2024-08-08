import unittest
from unittest.mock import patch, MagicMock
from processor.processor import Processor
import json


class TestProcessor(unittest.TestCase):

    @patch('processor.processor.boto3.client')
    @patch('processor.processor.sqlite3.connect')
    def test_process_message(self, mock_sqlite_connect, mock_boto_client):
        mock_db_conn = MagicMock()
        mock_sqlite_connect.return_value = mock_db_conn
        mock_cursor = mock_db_conn.cursor.return_value

        mock_message = {
            'Body': json.dumps({
                "location": {"name": "Test City", "country": "Test Country", "localtime": "2024-08-08 10:00"},
                "current": {"temp_c": 25, "condition": {"text": "Sunny"}}
            }),
            'ReceiptHandle': 'test-receipt-handle'
        }

        mock_sqs_client = MagicMock()
        mock_boto_client.return_value = mock_sqs_client
        mock_sqs_client.receive_message.return_value = {'Messages': [mock_message]}

        processor = Processor('your_access_key_id', 'your_secret_access_key')

        processor.background_task()

        mock_cursor.execute.assert_called_once_with(
            'INSERT INTO weather_data (localtime, name, country, temp_c, condition_text) VALUES (?, ?, ?, ?, ?)',
            ('2024-08-08 10:00', 'Test City', 'Test Country', 25, 'Sunny')
        )
        mock_sqs_client.delete_message.assert_called_once_with(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/858960673597/exercise-exodus',
            ReceiptHandle='test-receipt-handle'
        )


if __name__ == '__main__':
    unittest.main()