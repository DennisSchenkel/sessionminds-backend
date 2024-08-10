from rest_framework import permissions


# A custom permission that only allows the owner of an object to edit it.
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    # Read permissions are allowed to any request,
    # GET, HEAD or OPTIONS requests are allways allowed.
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the profile.
        return obj.user == request.user


class AllowAny(permissions.BasePermission):
    """
    Custom permission to allow any request.
    """

    def has_permission(self, request, view):
        return True
