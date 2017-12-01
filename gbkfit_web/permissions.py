# from django.core.exceptions import FieldError
from rest_framework import permissions
# from rest_framework.filters import BaseFilterBackend
# from rest_framework.permissions import SAFE_METHODS

from gbkfit_web.models import User, Job

def is_user(username):
    try:
        user = User.objects.get(username=username)
        user_role = user.role
    except (User.DoesNotExist) as e:
        user_role = None

    return True if user_role == User.IS_USER else False


def is_admin(username):
    try:
        user = User.objects.get(username=username)
        user_role = user.role
    except (User.DoesNotExist) as e:
        user_role = None

    return True if user_role == User.IS_ADMIN else False


class UserPlusPermission(permissions.BasePermission):
    """
    Permission to check member or moderator or admin access
    """
    message = "You must be at least a member to perform this action"

    def has_permission(self, request, view):
        return is_admin(request.user.username) or is_user(request.user.username)


class AdminOnlyPermission(permissions.BasePermission):
    """
    Permission to check admin access
    """
    message = "You must be an admin to perform this action"

    def has_permission(self, request, view):
        return is_admin(request.user.username)

class UserPlusWithUserOwnObject(UserPlusPermission):
    """
    Moderators and above get full permissions.
    Members can list / update / retrieve / partial_update objects if they own them
    """
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        try:
            if obj.user == request.user:
                return True
        except AttributeError:
            pass

        # Fallback to moderator plus
        return super(UserPlusWithUserOwnObject, self).has_permission(request, view)

    def has_permission(self, request, view):
        safe_actions = ['list', 'update', 'retrieve', 'partial_update', ]
        if view.action in safe_actions:
            return UserPlusPermission.has_permission(self, request, view)
        return super(UserPlusWithUserOwnObject, self).has_permission(request, view)


class UserPlusWithMemberOwnObjectWithCreate(UserPlusWithUserOwnObject):
    """
    Moderators and above get full permissions.
    Members can:
        1. create objects with their own reference. For example: create their own user-department
        2. update, list, retrieve, partial_update the objects if they own them
    """
    def has_permission(self, request, view):
        # if view.action in ['create']:
        if request.user.pk == request.data['user']:
            return UserPlusPermission.has_permission(self, request, view)
        return super(UserPlusWithMemberOwnObjectWithCreate, self).has_permission(request, view)
    
