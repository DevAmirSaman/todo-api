from django.urls import path

from .views import UserView, AvatarView

urlpatterns = [
    path('me/', UserView.as_view(), name='user-profile'),
    path('me/avatar/', AvatarView.as_view(), name='user-avatar'),
]
