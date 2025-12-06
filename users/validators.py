from rest_framework import serializers
import re


def validate_username(value):
    if not (6 <= len(value) <= 32):
        raise serializers.ValidationError('Username must be 6-32 characters long.')

    if not re.match(r'^[A-Za-z]', value):
        raise serializers.ValidationError('Username must start with a letter.')

    return value
