from django.urls import include, path

urlpatterns = [
    path("auth/", include("backend_auth.urls")),
    path("core/", include("core.urls")),
]
