import boto3
from boto3.exceptions import ResourceNotExistsError
from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource
import os
import pprint

from logger import log
from exceptions import MissingCredentialsError, InvalidCredentialsError

class AWSClient:
    __aws_region_name: str
    __aws_access_key: str
    __aws_secret_access_key: str

    def __init__(self) -> None:
        # setup region - can default to "eu-west-1"
        _aws_region_name = os.getenv("AWS_REGION", None)
        if not _aws_region_name:
            log("AWS_REGION env var is not set, defaulting to \"eu-west-1\"", logType="WARNING")
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
    
    def get_resource(self, resource_name: str) -> ServiceResource | None:
        try:
            return boto3.resource(
                resource_name,
                region_name=self.__aws_region_name,
                aws_access_key_id=self.__aws_access_key,
                aws_secret_access_key=self.__aws_secret_access_key,
            )
        except ResourceNotExistsError:
            log(f"Resource - \"{resource_name}\", does not exist", "WARNING")
            return
        except Exception as _err:
            raise InvalidCredentialsError()
    
    @staticmethod
    def get_resource_collections(resource: ServiceResource) -> list[str]:
        return [collection.name for collection in resource.meta.resource_model.collections]
    
    def display_metadata(self, user_input: str) -> None:
        resource_name = user_input.split(".")[0]

        resource = self.get_resource(resource_name)
        if resource == None:
            return
        
        resource_metadata = {}

        collections = [collection.name for collection in resource.meta.resource_model.collections]
        
        for collection_name in collections:
            try:
                instance_metadata = {}
                for service_instance in getattr(resource, collection_name).all():
                    try:
                        instance_metadata[service_instance.id] = service_instance.meta.data
                    except AttributeError as _err:
                        log(f"{resource_name}.{collection_name} does not have an instance of id", "WARNING")
                resource_metadata[collection_name] = instance_metadata
            except ClientError:
                log(f"IAM user does not have permission to view \"{resource_name}\" instances!", "ERROR")
                return
        
        pprint.pprint(resource_metadata)
