import io
import shutil
import tempfile

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework.test import APIClient

from tasks.models import Task

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    raw_password = 'password'
    u = User.objects.create_user(username='testuser', password='password')
    u.raw_password = raw_password
    return u


@pytest.fixture
def another_user(db):
    raw_password = 'password'
    u = User.objects.create_user(username='anotheruser', password='password')
    u.raw_password = raw_password
    return u


@pytest.fixture
def image():
    file = io.BytesIO()
    Image.new('RGB', (100, 100), color='red').save(file, format='PNG')
    file.seek(0)

    return SimpleUploadedFile(
        name='avatar.png', content=file.read(), content_type='image/png'
    )


@pytest.fixture(autouse=True)
def media_temp(settings):
    temp_dir = tempfile.mkdtemp()
    settings.MEDIA_ROOT = temp_dir
    yield
    shutil.rmtree(temp_dir)


@pytest.fixture
def todo_task(db, user):
    return Task.objects.create(
        title='To Do Task', status=Task.Status.TODO, user=user
    )


@pytest.fixture
def in_progress_task(db, user):
    return Task.objects.create(
        title='In Progress Task', status=Task.Status.IN_PROGRESS, user=user
    )


@pytest.fixture
def done_task(db, user):
    return Task.objects.create(
        title='Task Done', status=Task.Status.DONE, user=user
    )


@pytest.fixture
def todo_task_by_other_user(db, another_user):
    return Task.objects.create(
        title='To Do Task', status=Task.Status.TODO, user=another_user
    )
