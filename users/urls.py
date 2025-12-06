from django.urls import path

from .views import AvatarView, UserView

urlpatterns = [
    path('me/', UserView.as_view(), name='user-profile'),
    path('me/avatar/', AvatarView.as_view(), name='user-avatar'),
]
