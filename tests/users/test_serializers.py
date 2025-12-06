from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image
import pytest

from users.serializers import AvatarSerializer, UserSerializer


class TestAvatarSerializer:
    def test_serializer_rejects_too_large_images(self, image, monkeypatch):
        """Test that images exceeding the maximum file size are rejected."""
        monkeypatch.setattr(image, 'size', 3 * 1024 * 1024)

        serializer = AvatarSerializer(data={'avatar': image})

        assert not serializer.is_valid()
        assert 'Avatar file too large' in str(serializer.errors)

    def test_serializer_rejects_invalid_format(self):
        """Test that images not in JPEG or PNG format are rejected."""
        file = io.BytesIO()
        Image.new('RGB', (10, 10), color='red').save(file, format='GIF')
        file.seek(0)
        image = SimpleUploadedFile('avatar.gif', file.read(), content_type='image/gif')

        serializer = AvatarSerializer(data={'avatar': image})

        assert not serializer.is_valid()
        assert 'Only JPEG and PNG images are allowed.' in str(serializer.errors)


class TestUserSerializer:
    @pytest.mark.parametrize('username', [
        'abc',          # too short
        '1abcdef',      # starts with digit
        '_username',    # starts with symbol
        'a' * 33,       # too long
    ])
    def test_username_invalid(self, username):
        """Test that invalid usernames are rejected by the serializer."""
        serializer = UserSerializer(data={'username': username})
        assert not serializer.is_valid()
