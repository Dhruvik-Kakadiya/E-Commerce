from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admins to modify (create, update, delete) products,
    but allow everyone (authenticated or not) to view the product list.
    """

    def has_permission(self, request, view):
        # Allow any user to view (GET request) product list
        if request.method in ['GET']:
            return True

        # Only admin users can create, update, or delete products
        return request.user and request.user.is_staff
