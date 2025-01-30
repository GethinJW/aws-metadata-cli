import boto3
import os
from dotenv import load_dotenv
from termcolor import colored

load_dotenv()

class GenericError(Exception):
    msg: str

    def __init__(self, msg: str) -> None:
        self.msg = msg
        super()

class MissingCredentialsError(GenericError): pass
class InvalidCredentialsError(GenericError): pass

class AWSClient:
    __aws_region_name: str
    __aws_access_key: str
    __aws_secret_access_key: str

    def __init__(self) -> None:
        # setup region - can default to "eu-west-1"
        _aws_region_name = os.getenv("AWS_REGION", None)
        if not _aws_region_name:
            print(colored("WARNING!", "yellow"), " AWS_REGION env var is not set, defaulting to \"eu-west-1\"")
            _aws_region_name = "eu-west-1"
        self.__aws_region_name = _aws_region_name

        # setup access key - throw error if not found
        _aws_access_key = os.getenv("AWS_ACCESS_KEY_ID", None)
        if not _aws_access_key:
            raise MissingCredentialsError("Must set AWS_ACCESS_KEY_ID env var")
        self.__aws_access_key = _aws_access_key

        # setup secret access key - throw error if not found
        _aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", None)
        if not _aws_secret_access_key:
            raise MissingCredentialsError("Must set AWS_SECRET_ACCESS_KEY env var")
        self.__aws_secret_access_key = _aws_secret_access_key
    
    def get_resource(self, service_name: str):
        try:
            return boto3.resource(
                service_name,
                region_name=self.__aws_region_name,
                aws_access_key_id=self.__aws_access_key,
                aws_secret_access_key=self.__aws_secret_access_key,
            )
        except:
            raise InvalidCredentialsError()

if __name__ == "__main__":
    """Test Code"""
    aws_client = AWSClient()
    ec2_client = aws_client.get_resource("ec2")
    print(ec2_client.instances)
    # for x in ec2_client.__dir__():
    #     print(x)
