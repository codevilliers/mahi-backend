from django.urls import path

from mahi_auth.views.login import Login, CheckPhoneNumberExists
from mahi_auth.views.logout import Logout
from mahi_auth.views.delete import Delete
from mahi_auth.views.who_am_i import WhoAmIView
from mahi_auth.views.update import UpdateUser, SyncWithFirebaseView

urlpatterns = [
    path(
        'who_am_i/',
        WhoAmIView.as_view(),
        name='who_am_i'
    ),
    path(
        'phone_number_exists/',
        CheckPhoneNumberExists.as_view(),
        name='phone_number_exists'
    ),
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
    path(
        'delete_user/',
        Delete.as_view(),
        name='delete'
    ),
    path(
        'update_user/',
        UpdateUser.as_view(),
        name='update'
    ),
    path(
        'sync_with_firebase/',
        SyncWithFirebaseView.as_view(),
        name='sync_with_firebase'
    )
]
