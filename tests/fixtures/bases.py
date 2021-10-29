from builtins import isinstance
from collections import defaultdict
from enum import Enum
from typing import Type, Union

from django.db.models import Model
from model_bakery.recipe import Recipe as BakerRecipe


class Recipe(BakerRecipe):
    INSTANCES = defaultdict(lambda: [])

    def __init__(
        self,
        _model: Union[str, Model],
        _is_recreate: bool = False,
        *args,
        **kwargs,
    ) -> None:
        self._is_recreate = _is_recreate
        self._post_create = kwargs.pop("_post_create", None)
        self._quantity = kwargs.get("_quantity", 1)

        super().__init__(_model, *args, **kwargs)

    @property
    def instances(self):
        return self.INSTANCES[self]

    def make(self, *args, **kwargs) -> list[Model]:
        """If `self._is_recreate` is False, only create the object once.
        Returns:
            [Model]: The newly or already created instance
        """
        if not self._is_recreate and self.instances:
            instances = self.instances
        else:
            instances = super().make(*args, **kwargs)

            if self._quantity == 1:
                instances = [instances]

            if self._post_create:
                self._post_create(instances, self)

            self.instances.extend(instances)

        return instances[0] if self._quantity == 1 else instances


class RecipeFactory:
    def __init__(self, recipe_templates) -> None:
        self.recipes_templates = recipe_templates

    def make_by_template(self, template: Type[Enum]) -> list[Model]:
        recipe = self.recipes_templates[type(template)][template]
        instances = instances if isinstance(instances := recipe.make(), list) else [instances]
        return {
            "instances": instances,
            "template": recipe.attr_mapping,
        }

    @property
    def instances(self):
        return [
            instance
            for recipe_templates in self.recipes_templates.values()
            for recipe in recipe_templates.values()
            for instance in recipe.instances
        ]

    def clean(self):
        Recipe.INSTANCES = defaultdict(lambda: [])
