from django.db import models


class shelter(models.Model):
    # Define fields for YourModel
    id = models.CharField(max_length=254, unique=True, primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, blank=True)
    location = models.TextField(max_length=200, blank=True)
    contact = models.CharField(max_length=200, blank=True)
    size = models.CharField(max_length=200, blank=True)
    # Define other fields as needed for YourModel

    def __str__(self):
        return self.id

    class Meta:
        ordering = [
            "id",
        ]

