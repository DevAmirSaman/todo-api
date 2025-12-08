from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root(request, format=None):
    return Response(
        {
            'tasks': reverse('task-list', request=request, format=format),
            'user-profile': reverse(
                'user-profile', request=request, format=format
            ),
            'user-avatar': reverse(
                'user-avatar', request=request, format=format
            ),
            'signup': reverse('signup', request=request, format=format),
            'login': reverse('login', request=request, format=format),
        }
    )
