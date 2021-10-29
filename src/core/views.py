from rest_framework import viewsets

import core.models as cm
import core.permissions as cp
import core.serializers as cs


class BookViewSet(viewsets.ModelViewSet):
    queryset = cm.Book.objects.order_by("writer")
    serializer_class = cs.Book.Default
    permission_classes = [
        cp.Book.Default,
    ]
    filterset_fields = {
        "genre": [
            "exact",
            "in",
        ],
        "price": ["exact", "lte", "gte"],
    }
    search_fields = [
        "genre__name",
    ]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(writer=user)
