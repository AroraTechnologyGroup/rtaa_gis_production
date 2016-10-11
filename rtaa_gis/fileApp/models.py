from django.db import models


class GridCell(models.Model):
    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        ordering = ('name',)
        app_label = 'fileApp'

    name = models.CharField(
            max_length=25,
            primary_key=True,
    )


class FileModel(models.Model):

    def __unicode__(self):
        return "%s" % self.base_name

    class Meta:
        ordering = ('base_name', )
        app_label = 'fileApp'

    file_path = models.CharField(max_length=255, unique=True)

    base_name = models.CharField(max_length=255)

    file_type = models.CharField(max_length=25)

    mime = models.CharField(max_length=255)

    size = models.CharField(max_length=25)

    date_added = models.DateField(auto_now=True)

    grid_cells = models.ManyToManyField(GridCell,
                                        through='Assignment',
                                        through_fields=('file', 'grid_cell')
                                        )

    comment = models.CharField(max_length=255, null=True)


class Assignment(models.Model):
    def __unicode__(self):
        return "%s %s" % (self.grid_cell, self.file.name)

    class Meta:
        ordering = ('grid_cell', 'file', 'date_assigned', 'comment',)
        app_label = 'fileApp'

    grid_cell = models.ForeignKey(
            GridCell,
            on_delete=models.CASCADE,
            null=False
    )
    file = models.ForeignKey(
            FileModel,
            on_delete=models.CASCADE,
            null=False
    )

    base_name = models.CharField(max_length=50, null=True)

    date_assigned = models.DateField(auto_now_add=True,
                                     null=True)

    comment = models.CharField(
        max_length=255,
        null=True
    )
