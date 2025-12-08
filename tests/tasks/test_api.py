import pytest
from django.urls import reverse
from rest_framework import status

from tasks.models import Task


class TestTaskAPI:
    @pytest.mark.parametrize(
        'method,url_name',
        [
            ('get', 'task-list'),
            ('patch', 'task-list'),
            ('delete', 'task-list'),
        ],
    )
    def test_tasks_requires_authentication(self, api_client, method, url_name):
        """Test that the tasks endpoint is inaccessible without authentication."""
        url = reverse(url_name)

        response = getattr(api_client, method)(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_put_not_allowed_on_tasks(self, api_client, user):
        """Test that PUT method is not allowed on tasks endpoint."""
        api_client.force_authenticate(user=user)
        url = reverse('task-list')

        response = api_client.put(url, data={})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_user_associated_to_task(self, api_client, user):
        """Test that a created task is automatically associated with the authenticated user."""
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'Task description',
            'status': 'todo',
        }
        api_client.force_authenticate(user=user)

        response = api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED

        tasks = Task.objects.filter(user=user)
        assert tasks.exists()
        assert tasks.count() == 1

    def test_authenticated_user_can_list_only_their_own_tasks(
        self, api_client, user, todo_task, todo_task_by_other_user
    ):
        """Test that the authenticated user receives only their own tasks in the list response."""
        url = reverse('task-list')
        api_client.force_authenticate(user=user)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_tasks_are_ordered_by_status(
        self, api_client, user, done_task, in_progress_task, todo_task
    ):
        """Test that tasks are returned in the correct status order: in_progress → todo → done."""
        url = reverse('task-list')
        api_client.force_authenticate(user=user)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        statuses = [task['status'] for task in response.data['results']]
        assert statuses == ['in_progress', 'todo', 'done']

    def test_user_can_change_status_of_a_task(
        self, api_client, user, todo_task
    ):
        """Test that the authenticated user can update the status of their task."""
        url = reverse('task-detail', args=[todo_task.id])
        api_client.force_authenticate(user=user)
        data = {'status': 'in_progress'}

        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'in_progress'

    def test_user_cannot_access_another_users_task(
        self, api_client, user, todo_task_by_other_user
    ):
        """Test that a user cannot retrieve a task that belongs to someone else."""
        url = reverse('task-detail', args=[todo_task_by_other_user.id])
        api_client.force_authenticate(user=user)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_can_delete_task(self, api_client, user, todo_task):
        """Test that the authenticated user can delete their own task."""
        api_client.force_authenticate(user=user)
        url = reverse('task-detail', args=[todo_task.id])

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Task.objects.filter(id=todo_task.id).exists()

    @pytest.mark.parametrize('status_param', ['todo', 'done', 'in_progress'])
    def test_user_can_filter_tasks_by_status(
        self,
        api_client,
        user,
        todo_task,
        done_task,
        in_progress_task,
        status_param,
    ):
        """Test that the authenticated user can filter their tasks by status."""
        api_client.force_authenticate(user=user)
        url = reverse('task-list')

        response = api_client.get(url, {'status': status_param})

        assert response.status_code == status.HTTP_200_OK

        for task in response.data['results']:
            assert task['status'] == status_param
