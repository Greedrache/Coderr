from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it. This permission class allows read-only access to any user, 
    but only allows the owner of the object to make changes (PUT, PATCH, DELETE). The ownership is determined by comparing the user associated with
    the business of the object to the authenticated user making the request.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.business.user == request.user
