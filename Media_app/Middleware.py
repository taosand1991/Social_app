from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from django.shortcuts import reverse


class AdminRestrictMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            if request.user.is_authenticated:
                if not request.user.is_staff:
                    raise Http404

            else:
                raise Http404
