from django.contrib.auth import (
    get_user_model)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

__all__ = (
    'profile',
)

User = get_user_model()


@login_required
def profile(request):
    return HttpResponse(f'User profile page {request.user}')
