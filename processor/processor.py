import cmd
import threading
import time
from sqs_handler import SQSHandler
from database import Database

class Processor(cmd.Cmd):
    prompt = '(processor) '

    def __init__(self, aws_access_key_id, aws_secret_access_key):
        super().__init__()
        self._stop_event = threading.Event()
        self.sqs_handler = SQSHandler(aws_access_key_id, aws_secret_access_key)
        self.db = Database()
        self.db.create_table()
        self.background_thread = threading.Thread(target=self.background_task)
        self.background_thread.daemon = True
        self.background_thread.start()

    def fetch_message(self):
        return self.sqs_handler.fetch_message()

    def delete_message(self, receipt_handle):
        self.sqs_handler.delete_message(receipt_handle)

    def save_to_db(self, data):
        self.db.save_to_db(data)

    def process_message(self, message):
        data = self.sqs_handler.parse_message(message)
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
        self.db.close_connection()
        return True

    def do_status(self, arg):
        print("Background task is running.")

    def do_EOF(self, line):
        return self.do_exit(line)