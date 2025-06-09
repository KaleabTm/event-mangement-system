from django.contrib.auth import get_user_model
from django.db import models

from core.common.models import BaseModel

User = get_user_model()


# Create your models here.
class Calendar(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="calendars")
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7)  # "#FFFFFF"
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.user.email}"

    class Meta:
        verbose_name = "Calendar"
        verbose_name_plural = "Calendars"
