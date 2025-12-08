from django.db.models import Case, IntegerField, Value, When
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TasksViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        query_params = self.request.query_params

        if status_param := query_params.get('status'):
            queryset = queryset.filter(status__iexact=status_param)

        order_by_status = Case(
            When(status=Task.Status.IN_PROGRESS, then=Value(0)),
            When(status=Task.Status.TODO, then=Value(1)),
            When(status=Task.Status.DONE, then=Value(2)),
            output_field=IntegerField(),
        )

        return queryset.order_by(order_by_status)

    def update(self, request, *args, **kwargs):
        if not kwargs.get('partial', False):
            return Response(
                {'detail': 'PUT is not allowed. Use PATCH instead.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
