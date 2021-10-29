from django.urls import include, path

from backend.utils.misc import register_viewsets
from backend_auth import views as av

router = register_viewsets(av)

urlpatterns = [
    path("", include(router.urls)),
]
