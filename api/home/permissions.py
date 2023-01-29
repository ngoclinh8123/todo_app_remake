from rest_framework import permissions
from rest_framework import exceptions


class AddTodo(permissions.BasePermission):
    def has_permission(self, request, view):
        # cái home.add_todo tìm trong bảng phân quyền
        if not request.user.has_perm("home.add_todo"):
            raise exceptions.PermissionDenied("Don't have permission")
        return True
