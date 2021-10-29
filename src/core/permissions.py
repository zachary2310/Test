from rest_framework import permissions


class Book:
    class Default(permissions.BasePermission):
        def has_permission(self, request, view):
            if view.action == "partial_update":
                return False
            if request.user.is_anonymous:
                return view.action in ["list", "retrieve"]
            return super().has_permission(request, view)

        def has_object_permission(self, request, view, obj):
            if view.action in ["list", "retrieve"]:
                return True
            else:
                return obj.writer == request.user
