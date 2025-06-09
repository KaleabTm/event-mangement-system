from rest_framework import serializers


class RecurrenceRuleSerializer(serializers.Serializer):
    frequency = serializers.CharField()
    monthly_type = serializers.CharField()
    interval = serializers.IntegerField()
    weekdays = serializers.JSONField()
    weekday_ordinal = serializers.IntegerField()
    end_date = serializers.DateField()
    repeat_count = serializers.IntegerField()
