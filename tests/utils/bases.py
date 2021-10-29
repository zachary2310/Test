import json
import urllib
from datetime import datetime
from typing import Union
from uuid import UUID

from django.db.models import Model
from django.db.models.fields.files import ImageFieldFile
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.urls import reverse
from rest_framework.serializers import DateTimeField
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
)
from rest_framework.test import APIClient

import backend_auth.models as am


class TestBase:
    client = APIClient()

    not_accessible = {
        HTTP_401_UNAUTHORIZED,
        HTTP_403_FORBIDDEN,
        HTTP_404_NOT_FOUND,
        HTTP_405_METHOD_NOT_ALLOWED,
    }

    @staticmethod
    def __get_response_class(response):
        """APIClient returns diffrent types, each needs to be extended."""

        class Response(response.__class__):
            def __getitem__(self, header: Union[str, bytes]) -> str:
                try:
                    super().__getitem__(header)
                except KeyError:
                    return self.json()[header]

            @property
            def keys(self):
                return set(self.json().keys())

        return Response

    def __call_method(
        self,
        method: callable,
        name: str,
        user: am.BackendUser = None,
        token: str = "token",
        pk: Union[str, int] = None,
        format: str = "json",
        qs_params: str = None,
        *args: list,
        **kwargs: dict,
    ):
        # TODO:docstrings, types, exception handling
        if user:
            self.client.force_authenticate(user, token=token)
        else:
            self.client.logout()

        if "http" in name or name.startswith("/"):
            url = name
        else:
            url = reverse(name) if not pk else reverse(name, kwargs={"pk": pk})

        if qs_params:
            url = f"{url}?{urllib.parse.urlencode(qs_params)}"

        response = method(url, format=format, *args, **kwargs)
        response.__class__ = self.__get_response_class(response)
        return response

    def get(self, *args, **kwargs):
        return self.__call_method(self.client.get, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.__call_method(self.client.post, *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.__call_method(self.client.put, *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.__call_method(self.client.patch, *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.__call_method(self.client.delete, *args, **kwargs)

    def get_value(self, instance: Model, key: str, nested_map: dict = {}):
        def get_nested(child_instance, fields):
            if isinstance(fields, str):
                return self.get_value(child_instance, fields)
            else:
                return {field: self.get_value(child_instance, field) for field in fields}

        value = getattr(instance, key)

        if isinstance(value, Model):
            return get_nested(value, nested_map.get(key, "id"))
        if isinstance(value, datetime):
            return DateTimeField().to_representation(value)
        if isinstance(value, QuerySet):
            fields = nested_map.get(key, "id")
            return [get_nested(child_instance, fields) for child_instance in value]
        if isinstance(value, Manager):
            fields = nested_map.get(key, "id")
            return [get_nested(child_instance, fields) for child_instance in value.all()]
        if isinstance(value, UUID):
            return value.__str__()
        if isinstance(value, ImageFieldFile):
            return f"http://testserver{value.url}"

        return value

    def assert_deep(self, dict1, dict2):
        assert json.dumps(dict1, sort_keys=True, indent=2) == json.dumps(
            dict2, sort_keys=True, indent=2
        )
