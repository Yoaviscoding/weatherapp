import unittest
from unittest.mock import patch, MagicMock
from scheduler.scheduler import Scheduler

# Constants for AWS credentials
TEST_AWS_ACCESS_KEY_ID = 'AKIA4P7QLXM6WCU3ZNDS'
TEST_AWS_SECRET_ACCESS_KEY = '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'

class TestScheduler(unittest.TestCase):

    @patch('scheduler.sqs_handler.SQSHandler')
    @patch('scheduler.scheduler.Scheduler.read_cities', return_value=['Test City'])
    def test_read_cities(self, mock_read_cities, mock_sqs_handler):
        scheduler = Scheduler('scheduler/list_of_cities.txt', TEST_AWS_ACCESS_KEY_ID, TEST_AWS_SECRET_ACCESS_KEY)
        self.assertIn('Test City', scheduler.cities)

if __name__ == '__main__':
    unittest.main()