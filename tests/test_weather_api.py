# import unittest
# from unittest.mock import patch
# from scheduler.weather_api import fetch_weather
#
# class TestWeatherAPI(unittest.TestCase):
#
#     @patch('scheduler.weather_api.requests.get')
#     def test_fetch_weather(self, mock_get):
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.json.return_value = {
#             'location': {'localtime': '2023-08-08 12:00', 'name': 'Test City', 'country': 'Test Country'},
#             'current': {'temp_c': 25, 'condition': {'text': 'Sunny'}}
#         }
#
#         result = fetch_weather('Test City')
#         self.assertEqual(result['location']['name'], 'Test City')
#         self.assertEqual(result['current']['temp_c'], 25)
#         self.assertEqual(result['current']['condition']['text'], 'Sunny')
#
#     @patch('weather_api.requests.get')
#     def test_fetch_weather_failure(self, mock_get):
#         mock_get.return_value.status_code = 404
#
#         result = fetch_weather('Invalid City')
#         self.assertIsNone(result)
#
# if __name__ == '__main__':
#     unittest.main()