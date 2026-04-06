from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class OwnerOrStaffRequiredMixin(LoginRequiredMixin):
    """Allow access when the current user owns the object or is staff."""

    owner_field = 'owner'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        owner = getattr(obj, self.owner_field, None)
        if request.user.is_staff or owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied
