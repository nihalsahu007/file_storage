from rest_framework import permissions

class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_staff and not request.user.is_superuser