from rest_framework import permissions
from rest_framework import exceptions


class AddTodo(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.has_perm("add_todo"):
            raise exceptions.PermissionDenied("Don't have permission")
        return True


class ViewTodo(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.has_perm("view_todo"):
            raise exceptions.PermissionDenied("Don't have permission view todo")
        return True
