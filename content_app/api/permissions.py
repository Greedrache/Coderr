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

class IsCustomerOrBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow the customer who placed the order or the business providing it to access it.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
            
        user_profile = getattr(request.user, 'userprofile', None)
        if not user_profile:
            return False
            
        if request.method in permissions.SAFE_METHODS:
            return obj.customer_user == user_profile or obj.business_user == user_profile
            
        # Only the business user is allowed to modify the order (e.g. status)
        return obj.business_user == user_profile

class IsCustomer(permissions.BasePermission):
    """
    Permission to only allow customers to create or perform an action.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        user_profile = getattr(request.user, 'userprofile', None)
        return user_profile and user_profile.type == 'customer'

class IsBusiness(permissions.BasePermission):
    """
    Permission to only allow business profiles to create or perform an action.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        user_profile = getattr(request.user, 'userprofile', None)
        return user_profile and user_profile.type == 'business'
