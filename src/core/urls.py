from django.urls import include, path

import core.views as cv
from backend.utils.misc import register_viewsets

router = register_viewsets(cv)

urlpatterns = [path("", include(router.urls))]
