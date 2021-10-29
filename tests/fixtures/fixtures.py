import shutil
from enum import Enum

import pytest
from attr import dataclass
from django.conf import settings

from tests.fixtures import bases, recipes

FACTORY = bases.RecipeFactory(recipes.RECIPES)


@dataclass
class MakeResult:
    values: dict[Enum, dict]

    @property
    def instances(self):
        return [instance for value in self.values.values() for instance in value["instances"]]

    @property
    def templates(self):
        return [value["template"] for value in self.values.values()]

    def __getitem__(self, item):
        return self.values[item]


@pytest.fixture
def maker(db, request) -> MakeResult:
    result = {}
    for template in request.param[0]:
        result[template] = FACTORY.make_by_template(template)

    yield MakeResult(values=result)

    FACTORY.clean()


@pytest.fixture(scope="session", autouse=True)
def storage_cleaner():
    yield
    shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
