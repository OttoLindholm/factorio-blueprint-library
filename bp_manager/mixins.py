from django.http import HttpResponseForbidden

from bp_manager.models import User


class UserIsOwnerMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if isinstance(obj, User):
            if obj != self.request.user:
                return HttpResponseForbidden("You are not allowed to modify this user.")
            return obj

        if hasattr(obj, 'user') and obj.user != self.request.user:
            return HttpResponseForbidden("You are not allowed to modify this object.")

        return obj
