from rest_framework import serializers

import backend_auth.models as am
import core.serializers as cs


class BackendUser:
    class Default(serializers.ModelSerializer):
        Books = cs.Book.Default(many=True, read_only=True)

        class Meta:
            model = am.BackendUser
            fields = (
                "id",
                "username",
                "email",
                "first_name",
                "last_name",
                "Books",
            )
            read_only_fields = (
                "id",
                "username",
                "email",
                "first_name",
                "last_name",
                "Books",
            )
