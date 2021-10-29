from types import ModuleType

from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter


class BackendPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "pages_count": self.page.paginator.num_pages,
                "results": data,
            }
        )


def register_viewsets(
    views_module: ModuleType,
    excluded: list[str] = [],
) -> DefaultRouter:
    """Regsiters the viewsets automatically

    Args:
        views_module (ModuleType): Views module
        excluded (list[str]): A list of viewsets to exclude

    Return:
        DefaultRouter: The router
    """
    router = DefaultRouter()
    excluded += ["ModelViewSet", "GenericViewSet"]

    for viewset in filter(
        lambda x: x.endswith("ViewSet") and x not in excluded,
        dir(views_module),
    ):
        _class = getattr(views_module, viewset)
        path = viewset.replace("ViewSet", "").lower()
        basename = f"{_class.__module__.replace('.views','')}-{path}"
        router.register(path, _class, basename=basename)

    router.include_root_view = False
    return router
