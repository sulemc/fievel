from django.db import models
from uuid import uuid4

class Flagged_Ad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    url = models.CharField(max_length=500)
    location = models.CharField(max_length=100)
    mp_1_name = models.CharField(max_length=100)
    mp_1_url = models.CharField(max_length=500)
    mp_2_name = models.CharField(max_length=100)
    mp_2_url = models.CharField(max_length=500)
    mp_3_name = models.CharField(max_length=100)
    mp_3_url = models.CharField(max_length=500)
    mp_4_name = models.CharField(max_length=100)
    mp_4_url = models.CharField(max_length=500)
    mp_5_name = models.CharField(max_length=100)
    mp_5_url = models.CharField(max_length=500)

    def __str__(self):
        return self.url