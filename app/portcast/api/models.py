from django.db import models


class WordFrequency(models.Model):
    word = models.CharField(max_length=100, primary_key=True)
    frequency = models.IntegerField()

    class Meta:
        ordering = ['-frequency']
