import os
import time
import threading
import cmd
import boto3
import sqlite3
import json

class Processor(cmd.Cmd):
    prompt = '(processor) '

    def __init__(self, aws_access_key_id, aws_secret_access_key):
        super().__init__()
        self._stop_event = threading.Event()
        self.sqs_client = boto3.client(
            'sqs',
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.queue_url = 'https://sqs.us-east-1.amazonaws.com/858960673597/exercise-exodus'
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app', 'weather_data.db')
        self.db_connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.create_table()
        self.background_thread = threading.Thread(target=self.background_task)
        self.background_thread.daemon = True
        self.background_thread.start()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                localtime TEXT,
                name TEXT,
                country TEXT,
                temp_c REAL,
                condition_text TEXT
            )
        ''')
        self.db_connection.commit()

    def fetch_message(self):
        try:
            response = self.sqs_client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10
            )
            messages = response.get('Messages', [])
            if messages:
                return messages[0]
            return None
        except Exception as e:
            print(f"Error fetching message: {str(e)}")
            return None

    def delete_message(self, receipt_handle):
        try:
            self.sqs_client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
        except Exception as e:
            print(f"Error deleting message: {str(e)}")

    def save_to_db(self, data):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            INSERT INTO weather_data (localtime, name, country, temp_c, condition_text)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['localtime'], data['name'], data['country'], data['temp_c'], data['condition_text']))
        self.db_connection.commit()

    def process_message(self, message):
        body = json.loads(message['Body'])
        data = {
            'localtime': body['location']['localtime'],
            'name': body['location']['name'],
            'country': body['location']['country'],
            'temp_c': body['current']['temp_c'],
            'condition_text': body['current']['condition']['text']
        }
        self.save_to_db(data)

    def background_task(self):
        while not self._stop_event.is_set():
            message = self.fetch_message()
            if message:
                self.process_message(message)
                self.delete_message(message['ReceiptHandle'])
            if self._stop_event.is_set():
                break
            time.sleep(1)

    def do_exit(self, arg):
        print("Exiting...")
        self._stop_event.set()
        self.background_thread.join()
        self.db_connection.close()
        return True

    def do_status(self, arg):
        print("Background task is running.")

    def do_EOF(self, line):
        return self.do_exit(line)

if __name__ == '__main__':
    try:
        aws_access_key_id = 'AKIA4P7QLXM6WCU3ZNDS'
        aws_secret_access_key = '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'
        Processor(aws_access_key_id, aws_secret_access_key).cmdloop()
    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting gracefully.")