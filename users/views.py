from rest_framework import generics, status, views
from rest_framework.response import Response

from .models import CustomUser
from .serializers import AvatarSerializer, UserSerializer


class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        return self.request.user


class AvatarView(views.APIView):
    def patch(self, request):
        serializer = AvatarSerializer(
            instance=request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        user.avatar.delete(save=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
