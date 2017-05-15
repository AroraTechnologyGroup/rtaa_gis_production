from django.db import models


engineering_discipline_choices = (
        ('MISC', 'Miscellaneous'),
        ('CIVIL', 'Civil'),
        ('ARCH', 'Architectural'),
        ('STRUCTURAL', 'Structural'),
        ('LANDSCAPING', 'Landscaping'),
        ('MECHANICAL(HVAC)', 'Mechanical (HVAC)'),
        ('PLUMBING', 'Plumbing'),
        ('ELECTRICAL', 'Electrical')
    )

engineering_sheet_types = (
        ('DETAILS', 'Details'),
        ('PLAN', 'Plan'),
        ('TITLE', 'Title'),
        ('KEY', 'Key'),
        ('INDEX', 'Index'),
        ('ELEVATIONS', 'Elevations'),
        ('NOTES', 'Notes'),
        ('SECTIONS', 'Sections'),
        ('SYMBOLS', 'Symbols')
    )


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

    file_type = models.CharField(max_length=25)

    mime = models.CharField(max_length=255)

    size = models.CharField(max_length=25)

    date_added = models.DateField(auto_now=True)

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
    comment = models.CharField(
        max_length=255,
        blank=True
    )


class EngineeringDiscipline(models.Model):
    def __str__(self):
        return "{}".format(self.get_name_display())

    class Meta:
        ordering = ('name',)
        app_label = 'fileApp'

    name = models.CharField(max_length=125, blank=True, unique=True, choices=engineering_discipline_choices)


class EngineeringSheetType(models.Model):
    def __str__(self):
        return "{}".format(self.get_name_display())

    class Meta:
        ordering = ('name',)
        app_label = 'fileApp'

    name = models.CharField(max_length=125, blank=True, unique=True, choices=engineering_sheet_types)


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

    project_title = models.CharField(max_length=255)

    project_description = models.CharField(max_length=255, blank=True)

    project_date = models.DateField(null=True)

    sheet_title = models.CharField(max_length=255, blank=True)

    sheet_type = models.ManyToManyField(EngineeringSheetType)

    sheet_description = models.CharField(max_length=255, blank=True)

    vendor = models.CharField(max_length=255, blank=True)

    discipline = models.ManyToManyField(EngineeringDiscipline)

    airport = models.CharField(max_length=125, blank=True, choices=(
        ('RNO', 'Reno-Tahoe International Airport'),
        ('RTS', 'Reno/Stead Airport')
    ))

    funding_type = models.CharField(max_length=255, blank=True)

    grant_number = models.CharField(max_length=255, blank=True)


class EngineeringAssignment(Assignment):
    def __str__(self):
        return "%s %s" % (self.grid_cell, self.file)

    file = models.ForeignKey(
        EngineeringFileModel,
        on_delete=models.CASCADE,
        null=False
    )
