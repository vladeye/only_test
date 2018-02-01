from rest_framework import serializers
from .models import Readings

class ReadingsSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format"""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Readings
        fields = ('id', 'title', 'script', 'test', 'reads', 'status_api', 'status_reads', 'project_id', 'project_error', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')