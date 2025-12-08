from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TasksViewSet

router = DefaultRouter()
router.register(r'', TasksViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
