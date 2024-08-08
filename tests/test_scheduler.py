import unittest
from unittest.mock import patch, MagicMock
from scheduler.scheduler import Scheduler


class TestScheduler(unittest.TestCase):

    @patch('scheduler.scheduler.requests.get')
    @patch('scheduler.scheduler.boto3.client')
    def test_fetch_and_send_weather(self, mock_boto_client, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "location": {"name": "Test City", "country": "Test Country", "localtime": "2024-08-08 10:00"},
            "current": {"temp_c": 25, "condition": {"text": "Sunny"}}
        }
        mock_requests_get.return_value = mock_response

        mock_sqs_client = MagicMock()
        mock_boto_client.return_value = mock_sqs_client

        scheduler = Scheduler('list_of_cities.txt', 'your_access_key_id', 'your_secret_access_key')
        scheduler.cities = ['Test City']

        scheduler.background_task()

        mock_requests_get.assert_called_once_with(
            'http://api.weatherapi.com/v1/current.json?key=265960e484484c69be190222242307&q=Test City')
        mock_sqs_client.send_message.assert_called_once()


if __name__ == '__main__':
    unittest.main()