from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.CharField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'created_at', 'status', 'description']

    def validate_status(self, value):
        mapping = {}
        for choice_db, choice_display in Task.Status.choices:
            mapping[choice_display.lower()] = choice_db
            mapping[choice_db.lower()] = choice_db

        value = value.strip().lower()
        if value not in mapping:
            raise serializers.ValidationError(
                f'Invalid status value. Valid options: {", ".join(mapping.keys())}.'
            )

        return mapping[value]
