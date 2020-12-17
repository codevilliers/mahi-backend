from rest_framework import permissions


class IsVolunteer(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            is_volunteer = request.user.is_volunteer()
        except AttributeError:
            is_volunteer = False
        return is_volunteer
