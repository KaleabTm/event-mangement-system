from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.mixins import ApiAuthMixin
from core.calendar.models import Calendar
from core.calendar.serializers import CalendarSerializer
from core.users.serializers import UserSerializer

from .models import Event
from .selectors import get_event_by_id, get_user_events
from .serializers import RecurrenceRuleSerializer
from .services import event_create, event_delete, event_update


class EventListApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        user = UserSerializer()
        calendar = CalendarSerializer()
        title = serializers.CharField()
        description = serializers.CharField()
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()
        color = serializers.CharField(allow_null=True)
        is_all_day = serializers.BooleanField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
        recurrence = RecurrenceRuleSerializer()

    serializer_class = OutputSerializer

    def get(self, request):
        try:
            events = get_user_events(user=request.user)

            serializer = self.OutputSerializer(events, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            raise ValidationError(e)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        calendar_id = serializers.UUIDField()
        title = serializers.CharField(max_length=255)
        description = serializers.CharField(allow_blank=True)
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()
        color = serializers.CharField(max_length=7, allow_blank=True, required=False)
        is_all_day = serializers.BooleanField()
        frequency = serializers.CharField()
        interval = serializers.IntegerField(default=1)
        weekdays = serializers.JSONField(required=False, allow_null=True)
        weekday_ordinal = serializers.IntegerField(required=False, allow_null=True)
        end_date = serializers.DateField(required=False, allow_null=True)
        repeat_count = serializers.IntegerField(required=False, allow_null=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()
        color = serializers.CharField(allow_null=True)
        is_all_day = serializers.BooleanField()
        recurrence = RecurrenceRuleSerializer()

    serializer_class = InputSerializer

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            calendar = Calendar.objects.get(id=serializer.validated_data["calendar_id"])

            validated_data = serializer.validated_data

            validated_data.pop("calendar_id", None)

            event = event_create(
                user=request.user,
                calendar=calendar,
                **validated_data,
            )

            output_serializer = self.OutputSerializer(event)

            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            raise ValidationError(e)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()
        color = serializers.CharField(allow_null=True)
        is_all_day = serializers.BooleanField()
        recurrence = RecurrenceRuleSerializer()

    serializer_class = OutputSerializer

    def get(self, request, event_id):
        try:
            event = get_event_by_id(event_id=event_id)

            serializer = self.OutputSerializer(event)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            raise ValidationError(e)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        calendar_id = serializers.UUIDField()
        title = serializers.CharField(max_length=255)
        description = serializers.CharField(allow_blank=True)
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()
        color = serializers.CharField(max_length=7, allow_blank=True, required=False)
        is_all_day = serializers.BooleanField()
        frequency = serializers.CharField()
        interval = serializers.IntegerField(default=1)
        weekdays = serializers.JSONField(required=False, allow_null=True)
        weekday_ordinal = serializers.IntegerField(required=False, allow_null=True)
        end_date = serializers.DateField(required=False, allow_null=True)
        repeat_count = serializers.IntegerField(required=False, allow_null=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.UUIDField()
        title = serializers.CharField()
        description = serializers.CharField()
        start_time = serializers.DateTimeField()
        end_time = serializers.DateTimeField()
        color = serializers.CharField(allow_null=True)
        is_all_day = serializers.BooleanField()
        recurrence = RecurrenceRuleSerializer()

    serializer_class = InputSerializer

    def put(self, request, event_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            event = Event.objects.get(id=event_id, user=request.user)

            calendar = Calendar.objects.get(id=serializer.validated_data["calendar_id"])

            validated_data = serializer.validated_data

            validated_data.pop("calendar_id", None)

            updated_event = event_update(
                event=event,
                calendar=calendar,
                **validated_data,
            )

            output_serializer = self.OutputSerializer(updated_event)

            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except Event.DoesNotExist:
            raise NotFound("Event not found.")
        except Calendar.DoesNotExist:
            raise NotFound("Calendar not found.")
        except ValidationError as e:
            raise ValidationError(e)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, event_id):
        try:
            event_delete(event_id=event_id, user=request.user)

            return Response(status=status.HTTP_200_OK)

        except Event.DoesNotExist:
            raise NotFound("Event not found.")
        except ValidationError as e:
            raise ValidationError(e)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
