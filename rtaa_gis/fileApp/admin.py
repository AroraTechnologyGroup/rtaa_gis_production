from django.contrib import admin
from .models import GridCell, EngineeringFileModel, EngineeringAssignment, EngineeringDiscipline, EngineeringSheetType

admin.site.register(GridCell)
admin.site.register(EngineeringFileModel)
admin.site.register(EngineeringAssignment)
admin.site.register(EngineeringDiscipline)
admin.site.register(EngineeringSheetType)

