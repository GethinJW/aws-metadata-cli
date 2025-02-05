import json
import os

import boto3
from boto3.exceptions import ResourceNotExistsError
from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError

from exceptions import InvalidCredentialsError, MissingCredentialsError
from logger import log
from utils import get_nested_fields


class AWSClient:
    __aws_region_name: str
    __aws_access_key: str
    __aws_secret_access_key: str

    def __init__(self) -> None:
        # setup region - can default to "eu-west-1"
        _aws_region_name = os.getenv("AWS_REGION", None)
        if not _aws_region_name:
            log(
                'AWS_REGION env var is not set, defaulting to "eu-west-1"',
                logType="WARNING",
            )
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
            log(f'Resource - "{resource_name}", does not exist', "WARNING")
            return
        except Exception as _err:
            raise InvalidCredentialsError()

    @staticmethod
    def get_resource_collections(resource: ServiceResource) -> list[str]:
        return [
            collection.name for collection in resource.meta.resource_model.collections
        ]

    @staticmethod
    def get_resource_metadata_from_collection(
        resource_metadata: dict,
        resource: ServiceResource,
        resource_name: str,
        collection_name: str,
        fields: list[str],
    ) -> None:
        try:
            instance_metadata = {}
            for service_instance in getattr(resource, collection_name).all():
                try:
                    metadata = service_instance.meta.data
                    if fields:
                        info = {}
                        get_nested_fields(info, metadata, fields)
                    else:
                        info = metadata
                    instance_metadata[service_instance.id] = info
                except AttributeError as _err:
                    log(
                        f"{resource_name}.{collection_name} does not have an instance of id",
                        "WARNING",
                    )
                resource_metadata[collection_name] = instance_metadata
        except AttributeError as _err:
            log(
                f'resouce "{resource_name}", does not have collection: "{collection_name}"',
                "ERROR",
            )
            raise _err
        except ClientError as _err:
            log(
                f'IAM user does not have permission to view "{resource_name}" instances!',
                "ERROR",
            )
            raise _err

    def display_metadata(self, user_input: str) -> None:
        user_fields = user_input.split(".")

        resource_name = user_fields.pop(0)
        resource = self.get_resource(resource_name)
        if resource == None:
            return

        collection_name = None
        if user_fields:
            collection_name = user_fields.pop(0)

        resource_metadata = {}

        try:
            if collection_name:
                self.get_resource_metadata_from_collection(
                    resource_metadata=resource_metadata,
                    resource=resource,
                    resource_name=resource_name,
                    collection_name=collection_name,
                    fields=user_fields,
                )
            else:
                collections = [
                    collection.name
                    for collection in resource.meta.resource_model.collections
                ]
                for collection_name in collections:
                    self.get_resource_metadata_from_collection(
                        resource_metadata=resource_metadata,
                        resource=resource,
                        resource_name=resource_name,
                        collection_name=collection_name,
                    )
            print(json.dumps(resource_metadata, indent=4, default=str))
        except (
            ClientError,
            AttributeError,
        ):
            pass
