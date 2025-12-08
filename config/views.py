from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
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
