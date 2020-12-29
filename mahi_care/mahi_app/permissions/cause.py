from rest_framework import permissions


class CausePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['update', 'partial_update', 'destroy']:
            return False
        return True
