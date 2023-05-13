from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

def check_admin(role):

    if(role == '0' ):
        return True

class AdminPermissionMixin(LoginRequiredMixin):
    login_url = reverse_lazy('auth:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not check_admin(request.user.ocupation):
            return HttpResponseRedirect(
                reverse(
                    'home_app:home'
                )
            )
        return super().dispatch(request, *args, **kwargs)