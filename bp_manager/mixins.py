from bp_manager.models import User

from django.core.exceptions import PermissionDenied


class UserIsOwnerMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if isinstance(obj, User):
            if obj != self.request.user:
                raise PermissionDenied("You are not allowed to modify this user.")

        elif hasattr(obj, "user") and obj.user != self.request.user:
            raise PermissionDenied("You are not allowed to modify this object.")

        return obj
