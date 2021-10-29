from rest_framework.viewsets import GenericViewSet, mixins

import backend_auth.models as am
import backend_auth.permissions as ap
import backend_auth.serializers as as_


class BackendUserViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = am.BackendUser.objects.filter(
        is_active=True,
    ).order_by("id")
    permission_classes = [
        ap.BackendUser.Default,
    ]
    serializer_class = as_.BackendUser.Default
