from rest_framework import serializers

from core.common.utils import inline_serializer
from core.events.serializers import RecurrenceRuleSerializer


class CalendarSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    description = serializers.CharField()
    color = serializers.CharField()
    is_visible = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    events = inline_serializer(
        many=True,
        fields={
            "title": serializers.CharField(),
            "description": serializers.CharField(),
            "start_time": serializers.DateTimeField(),
            "end_time": serializers.DateTimeField(),
            "color": serializers.CharField(),
            "recurrence": RecurrenceRuleSerializer,
            "is_all_day": serializers.BooleanField(),
        },
    )
