from dotenv import load_dotenv

from aws_cli import AWSCLI
from aws_client import AWSClient

load_dotenv()

if __name__ == "__main__":
    aws_client = AWSClient()
    aws_cli = AWSCLI(aws_client)
    aws_cli.run()
