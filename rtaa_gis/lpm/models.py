from django.db import models


# Create your models here.
class AgreementModel(models.Model):
    """This is the active Agreement Model"""
    def __str__(self):
        return "%s" % self.title

    class Meta:
        ordering = ('title',)
        app_label = 'lpm'

    id = models.CharField(max_length=255, primary_key=True)

    title = models.CharField(max_length=255, unique=True)

    type = models.CharField(max_length=255)

    description = models.CharField(max_length=255)

    annual_revenue = models.CharField(max_length=255)

    contact1_name = models.CharField(max_length=255)

    contact1_phone_number = models.CharField(max_length=255)

    contact1_address = models.CharField(max_length=255)

    contact2_name = models.CharField(max_length=255)

    contact2_phone_number = models.CharField(max_length=255)

    contact2_address = models.CharField(max_length=255)

    start_date = models.DateField()

    end_date = models.DateField()
