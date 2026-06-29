from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Safe methods (GET, HEAD, OPTIONS) are allowed for ANY user (public).
    - Write methods (POST, PUT, PATCH, DELETE) require the user to be a staff member.
    """

    def has_permission(self, request, view):
        # Allow open read-only access
        if request.method in permissions.SAFE_METHODS:
            return True

        # Require authenticated staff account for editing database records
        return bool(request.user and request.user.is_staff)