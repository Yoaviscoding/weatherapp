import cmd
import threading
import time
from weather_api import fetch_weather
from sqs_handler import SQSHandler

class Scheduler(cmd.Cmd):
    prompt = '(scheduler) '

    def __init__(self, cities_file, aws_access_key_id, aws_secret_access_key):
        super().__init__()
        self._stop_event = threading.Event()
        self.cities = self.read_cities(cities_file)
        self.sqs_handler = SQSHandler(aws_access_key_id, aws_secret_access_key)
        self.background_thread = threading.Thread(target=self.background_task)
        self.background_thread.daemon = True
        self.background_thread.start()

    def read_cities(self, cities_file):
        with open(cities_file, 'r') as file:
            data = [line.strip() for line in file.readlines()]
            print(data)
            return data

    def fetch_weather(self, city):
        return fetch_weather(city)

    def send_to_sqs(self, message):
        self.sqs_handler.send_to_sqs(message)

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