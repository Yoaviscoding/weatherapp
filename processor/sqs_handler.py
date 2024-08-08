import boto3
import json

class SQSHandler:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.sqs_client = boto3.client(
            'sqs',
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.queue_url = 'https://sqs.us-east-1.amazonaws.com/858960673597/exercise-exodus'

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

    def parse_message(self, message):
        body = json.loads(message['Body'])
        return {
            'localtime': body['location']['localtime'],
            'name': body['location']['name'],
            'country': body['location']['country'],
            'temp_c': body['current']['temp_c'],
            'condition_text': body['current']['condition']['text']
        }