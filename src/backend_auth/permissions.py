from rest_framework import permissions


class BackendUser:
    class Default(permissions.BasePermission):
        def has_permission(self, request, view):
            if view.action == "partial_update":
                return False
            return super().has_permission(request, view)

        def has_object_permission(self, request, view, obj):
            if view.action == "retrieve":
                return True
            if view.action == "update":
                return obj == request.user
