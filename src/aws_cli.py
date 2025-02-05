import re

from logger import log
from aws_client import AWSClient

class AWSCLI:
    aws_client: AWSClient
    input_regex_pattern = r"^(?!.*\.\.)[a-z0-9_]+(\.[a-z0-9_]+)*$"

    def __init__(self, aws_client: AWSClient) -> None:
        self.aws_client = aws_client

    def run(self) -> None:
        while True:
            try:
                user_input = input(">")
                if user_input == "":
                    continue

                if not re.match(self.input_regex_pattern, user_input):
                    log("Input must be words (using lowercase letters, numbers, and hyphens) seperated by full stops", "WARNING")
                    continue

                if user_input == "exit":
                    break

                self.aws_client.display_metadata(user_input)
            except KeyboardInterrupt:
                break