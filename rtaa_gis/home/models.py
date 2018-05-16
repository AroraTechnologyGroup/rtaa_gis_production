from django.db import models
from django.contrib.auth.models import Group


# Create your models here.
class App(models.Model):
    def __str__(self):
        return "%s" % self.name

    class Meta:
        ordering = ('name',)
        app_label = 'home'

    name = models.CharField(
            max_length=25,
            primary_key=True
    )

    groups = models.ManyToManyField(Group)
