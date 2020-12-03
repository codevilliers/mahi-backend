from django.urls import path

from mahi_auth.views.login import Login
from mahi_auth.views.logout import Logout

urlpatterns = [
    path(
        'login/',
        Login.as_view(),
        name='login'
    ),
    path(
        'logout/',
        Logout.as_view(),
        name='logout'
    ),
]
