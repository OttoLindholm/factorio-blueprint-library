from django.http import HttpResponseForbidden


class UserIsOwnerMixin:

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            return HttpResponseForbidden("You are not allowed to modify this object.")
        return obj
