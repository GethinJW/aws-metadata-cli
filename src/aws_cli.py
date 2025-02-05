import re

from aws_client import AWSClient
from logger import log


class AWSCLI:
    aws_client: AWSClient
    input_regex_pattern = r"^(?!.*\.\.)[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*$"

    def __init__(self, aws_client: AWSClient) -> None:
        self.aws_client = aws_client

    def run(self) -> None:
        print(
            "Welcome to the AWS CLI - powered by the boto3 package!\n"
            'Type in a service name, i.e. "s3" to get metadata about it!\n'
            'For all information about a resource and specific collections, try typing something like "dynamodb.tables"\n'
            'For specific resource+collection+fields, try typing "ec2.instances.BlockDeviceMappings.Ebs.VolumeId"\n'
            'Type "exit", or Ctrl+C to quit\n'
        )
        while True:
            try:
                user_input = input(">")
                if user_input == "":
                    continue

                if not re.match(self.input_regex_pattern, user_input):
                    log(
                        "Input must be words (using letters, numbers, and hyphens) seperated by full stops",
                        "WARNING",
                    )
                    continue

                if user_input == "exit":
                    print("\n")
                    break

                self.aws_client.display_metadata(user_input)
            except (
                KeyboardInterrupt,
                EOFError,
            ):
                print("\n")
                break
