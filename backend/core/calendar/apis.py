# calendars/api.py

from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.common.utils import inline_serializer
from core.events.serializers import RecurrenceRuleSerializer

from .selectors import (
    get_all_calendars_for_user,
    get_calendar_by_id_for_user,
)
from .services import (
    calendar_create,
    calendar_delete,
    calendar_update,
)


class CalendarListApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
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
                "recurrence": RecurrenceRuleSerializer(),
                "is_all_day": serializers.BooleanField(),
            },
        )

    def get(self, request):
        try:
            calendars = get_all_calendars_for_user(user=request.user)

            serializer = self.OutputSerializer(calendars, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            # print("Validation error:", e)
            raise ValidationError(e)
        except Exception as e:
            # print("An unexpected error occurred:", e)
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CalendarCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        description = serializers.CharField(allow_blank=True)
        color = serializers.CharField(max_length=7)
        is_visible = serializers.BooleanField()

    class OutputSerializer(serializers.Serializer):
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

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            calendar = calendar_create(
                user=request.user,
                **serializer.validated_data,
            )

            output_serializer = self.OutputSerializer(calendar)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # print("ee", e)
            raise ValidationError(e)
        except Exception as e:
            # print("ee", e)
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CalendarDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
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
                "recurrence": RecurrenceRuleSerializer(),
                "is_all_day": serializers.BooleanField(),
            },
        )

    def get(self, request, calendar_id):
        try:
            calendar = get_calendar_by_id_for_user(calendar_id=calendar_id, user=request.user)
            serializer = self.OutputSerializer(calendar)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            raise ValidationError(e)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CalendarUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)
        description = serializers.CharField(allow_blank=True)
        color = serializers.CharField(max_length=7)
        is_visible = serializers.BooleanField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        name = serializers.CharField()
        description = serializers.CharField()
        color = serializers.CharField()
        is_visible = serializers.BooleanField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    def put(self, request, calendar_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            calendar = calendar_update(
                calendar_id=calendar_id,
                user=request.user,
                **serializer.validated_data,
            )

            output_serializer = self.OutputSerializer(calendar)
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            raise ValidationError(e)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CalendarDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, calendar_id):
        calendar_delete(calendar_id=calendar_id, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
