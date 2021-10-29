import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)

import core.models as cm
from tests.fixtures import BOOK_GENRES, BOOKS, USERS
from tests.utils import TestBase


class TestListingViewSet(TestBase):
    params_pagination = [(BOOKS.A, BOOKS.B)]
    params_patch = [(USERS.A,)]
    params_review = [(BOOKS)]
    params_filters = [
        (
            BOOKS.A,
            BOOKS.B,
            BOOKS.C,
        )
    ]

    @pytest.mark.parametrize("maker", [params_pagination], indirect=True)
    def test_pagination(self, maker):
        response = self.get("core-book-list")

        # Assert non enabled/approved are excluded
        assert response["count"] == 16
        assert response["pages_count"] == 2

        # Check pagination is working
        response = self.get(response["next"])

        assert len(response["results"]) == 6

    @pytest.mark.parametrize("maker", [params_patch], indirect=True)
    def test_patch_not_allowed(self, maker):
        user = maker.instances[0]

        response_patch_anonymous = self.patch(
            "core-book-detail",
            pk=1,
        )
        response_patch = self.patch(
            "core-book-detail",
            pk=1,
            user=user,
        )

        assert {
            response_patch_anonymous.status_code,
            response_patch.status_code,
        } <= self.not_accessible

    @pytest.mark.parametrize("maker", [params_filters], indirect=True)
    def test_filters(self, maker):
        book_a = maker[BOOKS.A]["instances"][0]
        book_b = maker[BOOKS.B]["instances"][0]

        numeric_filters = {
            "price": book_a.price,
        }
        filters = {
            "genre": book_a.genre.pk,
        }

        # Testing For Exact value
        for field, value in {**numeric_filters, **filters}.items():
            response_exact = self.get("core-book-list", qs_params={field: value})
            assert response_exact["count"] == 15

        # Testing for less than or equal value
        for field, value in numeric_filters.items():
            setattr(book_a, field, value - 1)
            book_a.save()

            response_lte = self.get("core-book-list", qs_params={f"{field}__lte": value - 1})
            assert response_lte["count"] == 2

        # Testing for greater than or equal value
        for field, value in numeric_filters.items():
            setattr(book_a, field, value + 1)
            book_a.save()

            response_lte = self.get("core-book-list", qs_params={f"{field}__gte": value + 1})

            assert response_lte["count"] == 2

        # Testing for in values
        qs_params = {"genre__in": f"{book_a.genre.pk},{book_b.genre.pk}"}
        response_in = self.get("core-book-list", qs_params=qs_params)
        assert response_in["count"] == 16

    @pytest.mark.parametrize("maker", [params_filters], indirect=True)
    def test_search(self, maker):
        book_a = maker[BOOKS.A]["instances"][0]

        # Testing for search value in genre
        qs_params = {"search": f"{book_a.genre.name}"}
        response_in = self.get("core-book-list", qs_params=qs_params)
        assert response_in["count"] == 15

    class TestAnonymousAndViewer(TestBase):
        params = [
            (
                BOOKS.A,
                USERS.B,
            )
        ]

        @pytest.mark.parametrize("maker", [params], indirect=True)
        def test_list_retreive(self, maker):
            book = maker[BOOKS.A]["instances"][0]

            pk_good = book.pk
            user = maker[USERS.B]["instances"][0]

            fields = {
                "writer",
                "name",
                "synopsis",
                "genre",
                "release_date",
                "price",
            }
            nested_map = {
                "writer": [
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                ],
            }
            fields_values = {
                key: self.get_value(maker.instances[0], key, nested_map) for key in fields
            }

            # Testing for anonymous and not owner
            for user_ in [user, None]:
                response_list = self.get("core-book-list", user=user_)
                response_detail_good = self.get("core-book-detail", pk=pk_good, user=user_)

                self.assert_deep(response_detail_good.json(), fields_values)
                self.assert_deep(response_list["results"][0], fields_values)
                assert response_list["count"] == 15

        @pytest.mark.parametrize("maker", [params], indirect=True)
        def test_cant_write(self, maker):
            pk = maker[BOOKS.A]["instances"][0].pk
            user = maker[USERS.B]["instances"][0]

            response_create_anonymous = self.post("core-book-list")
            response_update_anonymous = self.put("core-book-detail", pk=pk)
            response_update_viewer = self.put("core-book-detail", pk=pk, user=user)

            assert {
                response_update_viewer.status_code,
                response_create_anonymous.status_code,
                response_update_anonymous.status_code,
            } <= self.not_accessible

    class TestWriter(TestBase):
        params_retrieve = [(BOOKS.A,)]
        params_create = [
            (
                USERS.A,
                USERS.B,
                BOOK_GENRES.THRILLER,
            )
        ]
        params_update = [
            (
                BOOKS.B,
                BOOKS.A,
                BOOK_GENRES.THRILLER,
                USERS.A,
            )
        ]
        params_delete = [
            (
                BOOKS.A,
                BOOK_GENRES.ROMMAN,
                USERS.A,
            )
        ]

        @pytest.mark.parametrize("maker", [params_retrieve], indirect=True)
        def test_retrieve(self, maker):
            instance = maker[BOOKS.A]["instances"][0]
            user = instance.writer

            fields = {
                "writer",
                "name",
                "synopsis",
                "genre",
                "release_date",
                "price",
            }
            nested_map = {
                "writer": [
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                ],
            }
            fields_values = {
                key: self.get_value(
                    maker.instances[0],
                    key,
                    nested_map,
                )
                for key in fields
            }

            response = self.get("core-book-detail", pk=instance.pk, user=user)
            self.assert_deep(response.json(), fields_values)

        @pytest.mark.parametrize("maker", [params_create], indirect=True)
        def test_create(
            self,
            maker,
        ):

            user = maker.values[USERS.A]["instances"][0]

            book_genre = maker.values[BOOK_GENRES.THRILLER]["instances"][0]

            required_fields = {
                "price": 300.0,
                "genre": book_genre.pk,
                "synopsis": "this is synop",
                "name": "book name",
                "release_date": "2021-10-29T12:30:58.831431Z",
            }

            bad_fields = {
                "price": -200,
                "synopsis": "",
                "name": "",
            }

            response_not_optional = self.post("core-book-list", data=required_fields, user=user)
            response_not_required = self.post("core-book-list", user=user)

            response_validation = self.post(
                "core-book-list",
                data={**required_fields, **bad_fields},
                user=user,
            )

            assert response_not_optional.status_code == HTTP_201_CREATED

            assert response_not_required.status_code == HTTP_400_BAD_REQUEST
            assert response_not_required.keys == set(required_fields.keys())

            assert response_validation.status_code == HTTP_400_BAD_REQUEST
            assert response_validation.keys == set(bad_fields.keys())

            assert cm.Book.objects.count() == 1

        @pytest.mark.parametrize("maker", [params_update], indirect=True)
        def test_update(self, maker):
            book = maker[BOOKS.A]["instances"][0]
            book_genre = maker[BOOK_GENRES.THRILLER]["instances"][0]

            user = book.writer

            required_fields = {
                "price": 100,
                "genre": book_genre.pk,
                "synopsis": "this is synop",
                "name": "book name",
                "release_date": "2021-10-29T12:30:58.831431Z",
            }

            bad_fields = {
                "price": -1,
                "synopsis": "",
                "name": "",
            }

            # Test updated

            response = self.put(
                "core-book-detail",
                data=required_fields,
                user=user,
                pk=book.pk,
            )
            book.refresh_from_db()
            assert response.status_code == HTTP_200_OK

            # Test required not sent
            response = self.put("core-book-detail", data={}, user=user, pk=book.pk)
            assert response.status_code == HTTP_400_BAD_REQUEST

            assert response.keys == set(required_fields.keys())

            # Assert validation
            response = self.put(
                "core-book-detail",
                data={**required_fields, **bad_fields},
                user=user,
                pk=book.pk,
            )
            assert response.status_code == HTTP_400_BAD_REQUEST
            assert response.keys == set(bad_fields.keys())

        @pytest.mark.parametrize("maker", [params_delete], indirect=True)
        def test_delete(self, maker):
            book = maker[BOOKS.A]["instances"][0]
            user = book.writer

            response_delete = self.delete("core-book-detail", pk=book.pk, user=user)
            response_cant_retrieve = self.get("core-book-detail", pk=book.pk, user=user)
            response_not_in_list = self.get("core-book-list", user=user)

            assert response_delete.status_code == HTTP_204_NO_CONTENT
            assert response_cant_retrieve.status_code in self.not_accessible
            assert response_not_in_list["count"] == 14
