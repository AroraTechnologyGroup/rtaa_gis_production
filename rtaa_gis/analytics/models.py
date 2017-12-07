from django.db import models


class Record(models.Model):
    def __str__(self):
        return "{} / {} / {}".format(self.app_name, self.method, self.username)

    class Meta:
        ordering = ('method', 'username', 'date_time')
        app_label = 'analytics'

    app_choices = (
        ('fileApp', 'fileApp'),
        ('Print', 'Print'),
    )

    action_choices = (
        ('print', 'print'),
        ('download', 'download')
    )

    app_name = models.CharField(max_length=25, choices=app_choices)

    username = models.CharField(max_length=255, editable=False)

    method = models.CharField(max_length=25, choices=action_choices)

    date_time = models.DateTimeField(auto_now_add=True, editable=False)
