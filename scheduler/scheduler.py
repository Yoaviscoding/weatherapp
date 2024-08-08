import time
import threading
import cmd
import requests
import boto3
import json

class Scheduler(cmd.Cmd):
    prompt = '(scheduler) '

    def __init__(self, cities_file, aws_access_key_id, aws_secret_access_key):
        super().__init__()
        self._stop_event = threading.Event()
        self.cities = self.read_cities(cities_file)
        self.sqs_client = boto3.client(
            'sqs',
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.queue_url = 'https://sqs.us-east-1.amazonaws.com/858960673597/exercise-exodus'
        self.api_key = '265960e484484c69be190222242307'
        self.background_thread = threading.Thread(target=self.background_task)
        self.background_thread.daemon = True
        self.background_thread.start()

    def read_cities(self, cities_file):
        with open(cities_file, 'r') as file:
            data = [line.strip() for line in file.readlines()]
            print(data)
            return data

    def fetch_weather(self, city):
        url = f'http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={city}'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch weather data for {city}. Status code: {response.status_code}")
            return None

    def send_to_sqs(self, message):
        try:
            response = self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message)
            )
            print(f"Message sent to SQS: {response['MessageId']}")
        except Exception as e:
            print(f"Failed to send message to SQS: {str(e)}")

    def background_task(self):
        while not self._stop_event.is_set():
            for city in self.cities:
                weather_data = self.fetch_weather(city)
                if weather_data:
                    self.send_to_sqs(weather_data)
                if self._stop_event.is_set():
                    break
                time.sleep(60)

    def do_exit(self, arg):
        print("Exiting...")
        self._stop_event.set()
        self.background_thread.join()
        return True

    def do_status(self, arg):
        print("Background task is running.")

    def do_EOF(self, line):
        return self.do_exit(line)

if __name__ == '__main__':
    try:
        cities_file = 'list_of_cities.txt'
        aws_access_key_id = 'AKIA4P7QLXM6WCU3ZNDS'
        aws_secret_access_key = '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'
        Scheduler(cities_file, aws_access_key_id, aws_secret_access_key).cmdloop()
    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting gracefully.")