import pytest

from tasks.serializers import TaskSerializer


class TestTaskSerializer:
    @pytest.mark.parametrize(
        'input,expected',
        [
            ('in progress', 'in_progress'),
            ('In Progress', 'in_progress'),
            ('IN_PROGRESS', 'in_progress'),
            ('todo', 'todo'),
            ('To Do', 'todo'),
        ],
    )
    def test_validate_status_valid(self, input, expected):
        """Test that validate_status normalizes various valid inputs to the correct DB value."""
        serializer = TaskSerializer()

        assert serializer.validate_status(input) == expected

    def test_validate_status_invalid(self):
        """Test that validate_status raises an error for an invalid status value."""
        serializer = TaskSerializer()

        with pytest.raises(Exception) as exc:
            serializer.validate_status('not-a-status')

        assert 'Invalid status value' in str(exc.value)
