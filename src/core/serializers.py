from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

import backend_auth.models as am
import core.models as cm


class User:
    class Detail(serializers.ModelSerializer):
        class Meta:
            model = am.BackendUser
            fields = (
                "username",
                "email",
                "first_name",
                "last_name",
            )


class BookGenre:
    class Default(serializers.ModelSerializer):
        class Meta:
            model = cm.BookGenre
            fields = ["id", "name"]


class Book:
    class Default(WritableNestedModelSerializer):
        writer = User.Detail(read_only=True)

        class Meta:
            model = cm.Book
            fields = (
                "writer",
                "name",
                "synopsis",
                "genre",
                "release_date",
                "price",
            )
