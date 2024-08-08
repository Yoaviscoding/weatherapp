from processor import Processor

if __name__ == '__main__':
    try:
        aws_access_key_id = 'AKIA4P7QLXM6WCU3ZNDS'
        aws_secret_access_key = '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'
        Processor(aws_access_key_id, aws_secret_access_key).cmdloop()
    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting gracefully.")