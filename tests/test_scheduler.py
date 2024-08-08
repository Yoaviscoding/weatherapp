import unittest
from unittest.mock import patch, MagicMock
from scheduler.scheduler import Scheduler

# Constants for AWS credentials
TEST_AWS_ACCESS_KEY_ID = 'AKIA4P7QLXM6WCU3ZNDS'
TEST_AWS_SECRET_ACCESS_KEY = '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'

class TestScheduler(unittest.TestCase):

    @patch('scheduler.scheduler.SQSHandler')
    @patch('scheduler.scheduler.fetch_weather')
    def test_background_task(self, mock_fetch_weather, mock_sqs_handler):
        mock_fetch_weather.return_value = {
            'location': {'localtime': '2023-08-08 12:00', 'name': 'Test City', 'country': 'Test Country'},
            'current': {'temp_c': 25, 'condition': {'text': 'Sunny'}}
        }
        mock_sqs_handler_instance = mock_sqs_handler.return_value
        scheduler = Scheduler('scheduler/list_of_cities.txt', TEST_AWS_ACCESS_KEY_ID, TEST_AWS_SECRET_ACCESS_KEY)
        scheduler.cities = ['Test City']
        scheduler._stop_event.set()  # To stop the loop after one iteration

        scheduler.background_task()

        mock_fetch_weather.assert_called_once_with('Test City')
        mock_sqs_handler_instance.send_to_sqs.assert_called_once_with(mock_fetch_weather.return_value)

    @patch('scheduler.scheduler.SQSHandler')
    def test_read_cities(self, mock_sqs_handler):
        scheduler = Scheduler('scheduler/list_of_cities.txt', TEST_AWS_ACCESS_KEY_ID, TEST_AWS_SECRET_ACCESS_KEY)
        self.assertIn('Test City', scheduler.cities)

if __name__ == '__main__':
    unittest.main()