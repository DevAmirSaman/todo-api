from rest_framework import serializers

from .models import CustomUser
from .validators import validate_username


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(read_only=True)
    username = serializers.CharField(validators=[validate_username])

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar']


class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = ['avatar']

    def validate_avatar(self, value):
        if value.size > 1024 * 1024:
            raise serializers.ValidationError('Avatar file too large. Max 1MB allowed.')

        if value.content_type not in ['image/jpeg', 'image/png']:
            raise serializers.ValidationError('Only JPEG and PNG images are allowed.')

        return value
