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

    def send_to_sqs(self, message):
        try:
            response = self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message)
            )
            print(f"Message sent to SQS: {response['MessageId']}")
        except Exception as e:
            print(f"Failed to send message to SQS: {str(e)}")