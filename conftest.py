import pytest

pytest.register_assert_rewrite("tests.utils.bases")

from tests.fixtures import BOOKS, USERS, maker, storage_cleaner  # noqa: F401,E402
