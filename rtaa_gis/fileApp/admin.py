from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import GridCell, EngineeringFileModel, EngineeringAssignment, DocumentTypeModel, DisciplineModel,\
    SheetTypeModel


admin.site.register(GridCell)
admin.site.register(EngineeringFileModel)
admin.site.register(EngineeringAssignment)
admin.site.register(DocumentTypeModel)
admin.site.register(DisciplineModel)
admin.site.register(SheetTypeModel)


