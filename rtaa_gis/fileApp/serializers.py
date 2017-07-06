from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import GridCell, EngineeringAssignment, EngineeringFileModel
from .utils import function_definitions
import mimetypes
import os

engineering_discipline_choices = [
        ('MISC', 'Miscellaneous'),
        ('CIVIL', 'Civil'),
        ('ARCH', 'Architectural'),
        ('STRUCTURAL', 'Structural'),
        ('LANDSCAPING', 'Landscaping'),
        ('MECHANICAL(HVAC)', 'Mechanical (HVAC)'),
        ('PLUMBING', 'Plumbing'),
        ('ELECTRICAL', 'Electrical')
    ]

engineering_sheet_types = [
        ('DETAILS', 'Details'),
        ('PLAN', 'Plan'),
        ('TITLE', 'Title'),
        ('KEY', 'Key'),
        ('INDEX', 'Index'),
        ('ELEVATIONS', 'Elevations'),
        ('NOTES', 'Notes'),
        ('SECTIONS', 'Sections'),
        ('SYMBOLS', 'Symbols')
    ]


class GridSerializer(serializers.ModelSerializer):

    class Meta:
        model = GridCell
        fields = ('name',)
        read_only_fields = ('name',)

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class EngFileHyperLinkedRelatedField(serializers.HyperlinkedRelatedField):
    queryset = EngineeringFileModel.objects.all()
    view_name = 'engineeringfilemodel-detail'
    lookup_field = 'pk'
    many = True

    def display_value(self, instance):
        return instance.file_path


class GridPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    queryset = GridCell.objects.all()
    many = True
    pk_field = 'Name'

    def display_value(self, instance):
        return '%s' % instance.name


class EngineeringDisciplinesField(serializers.MultipleChoiceField):
    choices = engineering_discipline_choices
    allow_blank = True


class EngineeringSheetTypesField(serializers.MultipleChoiceField):
    choices = engineering_sheet_types
    allow_blank = True


class EngAssignmentSerializer(serializers.ModelSerializer):

    grid_cell = GridPrimaryKeyRelatedField()

    file = EngFileHyperLinkedRelatedField()

    class Meta:
        model = EngineeringAssignment
        fields = ('pk', 'grid_cell', 'file', 'base_name', 'comment', 'date_assigned')
        depth = 1
        read_only_fields = ('base_name', 'date_assigned')

    def create(self, validated_data):
        base_name = validated_data['file'].base_name
        return EngineeringAssignment.objects.create(base_name=base_name, **validated_data)

    def update(self, instance, validated_data):
        instance.grid_cell = validated_data.get('grid_cell', instance.grid_cell)
        instance.file = validated_data.get('file', instance.file)
        instance.base_name = os.path.basename(instance.file.file_path)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class EngSerializer(serializers.ModelSerializer):

    class Meta:
        model = EngineeringFileModel
        fields = ('pk', 'base_name', 'grid_cells', 'file_type', 'size', 'date_added', 'sheet_title', 'sheet_type',
                  'project_title', 'project_description', 'project_date', 'sheet_description', 'vendor', 'discipline',
                  'airport', 'funding_type', 'grant_number', 'file_path')
        depth = 1
        read_only_fields = ('pk', 'base_name', 'grid_cells', 'file_type', 'size', 'date_added', 'mime')

    grid_cells = serializers.SerializerMethodField()

    sheet_type = EngineeringSheetTypesField

    discipline = EngineeringDisciplinesField

    @staticmethod
    def get_grid_cells(self):
        base_name = self.base_name
        file_path = self.file_path
        assigns = EngineeringAssignment.objects.filter(base_name=base_name)
        grids = []
        for entry in assigns:
            _file = entry.file
            path = _file.file_path
            if path == file_path:
                _grid = entry.grid_cell
                if _grid.name not in grids:
                    grids.append(_grid.name)
        grids.sort()
        cells = ", ".join(grids)
        return cells

    def create(self, validated_data):
        file_path = validated_data['file_path']
        if os.path.exists(file_path):
            base_name = os.path.basename(file_path)
            file_type = base_name.split(".")[-1]
            size = function_definitions.convert_size(os.path.getsize(file_path))
            # TODO-use the same mimetype assigning done in the Build FileStore script
            mime = mimetypes.guess_type(file_path)[0]
            if mime is None:
                mime = ''
            comment = validated_data['comment']
        else:
            base_name = file_path.split("\\")[-1]
            file_type = base_name.split(".")[-1]
            size = ''
            mime = ''
            comment = 'eDoc system unable to locate file using the file_path'
        _file = EngineeringFileModel.objects.create(
            file_path=file_path,
            base_name=base_name,
            file_type=file_type,
            size=size,
            mime=mime,
            comment=comment
        )

        _file.save()
        return _file

    def update(self, instance, validated_data):
        file_path = validated_data.get('file_path', instance.file_path)
        instance.file_path = file_path
        if os.path.exists(file_path):
            base_name = os.path.basename(file_path)
            instance.base_name = base_name
            instance.file_type = base_name.split(".")[-1]
            instance.size = function_definitions.convert_size(os.path.getsize(file_path))
            instance.mime = mimetypes.guess_type(file_path)[0]
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance
