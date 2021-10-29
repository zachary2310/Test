import pytest
from rest_framework.status import HTTP_200_OK

from tests.fixtures import USERS
from tests.utils import TestBase


class TestBackendUserViewSet(TestBase):
    params_not_allowed = [[USERS.A, USERS.B]]
    params_retrieve = [
        [
            USERS.A,
            USERS.B,
        ]
    ]

    @pytest.mark.parametrize("maker", [params_not_allowed], indirect=True)
    def test_list_create_destroy_not_allowed(self, maker):
        user_a = maker[USERS.A]["instances"][0]
        user_b = maker[USERS.B]["instances"][0]

        url_list = "/api/v1/auth/backenduser/"
        url_detail = "backend_auth-backenduser-detail"

        for user in [None, user_a, user_b]:
            response_list = self.get(url_list, user=user)
            response_create = self.post(url_list, user=user)
            response_patch = self.patch(url_detail, user=user, pk=user_b.pk)
            response_delete = self.delete(url_detail, user=user, pk=user_b.pk)

            assert {
                response_list.status_code,
                response_create.status_code,
                response_patch.status_code,
                response_delete.status_code,
            } <= self.not_accessible

    @pytest.mark.parametrize("maker", [params_retrieve], indirect=True)
    def test_retrieve(self, maker):
        user_a = maker[USERS.A]["instances"][0]
        user_b = maker[USERS.B]["instances"][0]

        url_detail = "backend_auth-backenduser-detail"
        fields = {
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        }

        for user in [None, user_a, user_b]:
            response = self.get(url_detail, user=user, pk=user_b.pk)

            assert response.status_code == HTTP_200_OK
            assert response.keys == fields

    @pytest.mark.parametrize("maker", [params_retrieve], indirect=True)
    def test_update(self, maker):
        user_a = maker[USERS.A]["instances"][0]
        user_b = maker[USERS.B]["instances"][0]

        url_detail = "backend_auth-backenduser-detail"
        fields = {
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        }
        values_good = {
            "first_name": "A first name",
            "last_name": "A last name",
        }
        readonly_fields = {
            "username": "new_username",
            "email": "new_email@email.com",
        }

        response_good = self.put(
            url_detail,
            data=values_good | readonly_fields,
            user=user_b,
            pk=user_b.pk,
        )
        response_cant_viewer = self.put(url_detail, user=user_a, pk=user_b.pk)
        response_cant_anonymous = self.put(url_detail, pk=user_b.pk)

        assert response_good.status_code == HTTP_200_OK
        assert response_good.keys == fields

        assert {
            "username": user_b.username,
            "email": user_b.email,
        }.items() <= response_good.json().items()
        assert response_cant_viewer.status_code in self.not_accessible
        assert response_cant_anonymous.status_code in self.not_accessible
