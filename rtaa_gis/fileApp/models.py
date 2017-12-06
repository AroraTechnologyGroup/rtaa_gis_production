from django.db import models
from .utils.domains import FileTypes
from django.contrib.auth.models import User


ftypes = FileTypes()


class GridCell(models.Model):
    def __str__(self):
        return "%s" % self.name

    class Meta:
        ordering = ('name',)
        app_label = 'fileApp'

    name = models.CharField(
            max_length=25,
            primary_key=True,
    )


class DisciplineModel(models.Model):
    """This Model is used to relate files to standard CAD Disciplines"""
    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        app_label = 'fileApp'

    name = models.CharField(
        max_length=50,
        primary_key=True
    )

    label = models.CharField(
        max_length=50
    )


class DocumentTypeModel(models.Model):
    """This model is used to relate files to multiple standard document types"""
    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        app_label = 'fileApp'

    name = models.CharField(
        max_length=50,
        primary_key=True
    )

    label = models.CharField(
        max_length=50
    )


class SheetTypeModel(models.Model):
    """This model is used to relate files to multiple standard CAD sheet types"""
    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        app_label = 'fileApp'

    name = models.CharField(
        max_length=50,
        primary_key=True
    )

    label = models.CharField(
        max_length=50
    )


class FileModel(models.Model):
    """This Model is an abstract used to create other types of file object tables"""
    def __str__(self):
        return "%s" % self.base_name

    class Meta:
        ordering = ('base_name', )
        app_label = 'fileApp'
        abstract = True

    file_path = models.CharField(max_length=255, unique=True)

    base_name = models.CharField(max_length=255)

    file_type = models.CharField(max_length=25, choices=ftypes.ALL_FILE_DOMAINS)

    document_type = models.ManyToManyField(DocumentTypeModel, default=["unk"])

    mime = models.CharField(max_length=255)

    size = models.CharField(max_length=25)

    date_added = models.DateField(auto_now_add=True)

    last_edited_date = models.DateField(auto_now=True)

    last_edited_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    comment = models.CharField(max_length=255, blank=True)


class Assignment(models.Model):
    def __str__(self):
        return "%s" % self.grid_cell

    class Meta:
        ordering = ('grid_cell', 'file', 'date_assigned', 'comment',)
        app_label = 'fileApp'
        abstract = True

    grid_cell = models.ForeignKey(
            GridCell,
            on_delete=models.CASCADE,
            null=False
    )

    base_name = models.CharField(max_length=50, blank=True)

    date_assigned = models.DateField(auto_now_add=True,
                                     null=True)

    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    comment = models.CharField(
        max_length=255,
        blank=True
    )


# Models that inherit from the above
class EngineeringFileModel(FileModel):
    def __str__(self):
        return "{}".format(self.base_name)

    class Meta:
        ordering = ('project_title', 'project_date', 'sheet_title', 'vendor')

    grid_cells = models.ManyToManyField(GridCell,
                                        through='EngineeringAssignment',
                                        through_fields=('file', 'grid_cell')
                                        )

    project_title = models.CharField(max_length=255, null=True, blank=True)

    project_description = models.CharField(max_length=255, null=True, blank=True)

    project_date = models.DateField(null=True, blank=True)

    sheet_title = models.CharField(max_length=255, null=True, blank=True)

    sheet_type = models.ManyToManyField(SheetTypeModel, default=["unk"])

    sheet_description = models.CharField(max_length=255, blank=True)

    vendor = models.CharField(max_length=255, null=True, blank=True)

    discipline = models.ManyToManyField(DisciplineModel, default=["unk"])

    # the model serializer will automatically consume these choices
    airport = models.CharField(max_length=125, blank=True, choices=(
        ('rno', 'Reno-Tahoe International Airport'),
        ('rts', 'Reno/Stead Airport')
    ))

    funding_type = models.CharField(max_length=255, null=True, blank=True)

    grant_number = models.CharField(max_length=255, null=True, blank=True)


# This model inherits from above
class EngineeringAssignment(Assignment):
    def __str__(self):
        return "%s %s" % (self.grid_cell, self.file)

    class Meta:
        unique_together = (("file", "grid_cell"),)

    file = models.ForeignKey(
        EngineeringFileModel,
        on_delete=models.CASCADE,
        null=False
    )
