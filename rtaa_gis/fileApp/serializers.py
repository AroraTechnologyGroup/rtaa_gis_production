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
                ('MECHANICAL-HVAC', 'Mechanical-HVAC'),
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


class FileTypes:
    """the type of files that we are interested in are defined here"""

    def __init__(self):
        pdf = {"pdf": "application/pdf"}
        odt = {"odt": "application/vnd.oasis.opendocument.text"}
        ods = {"ods": "application/vnd.oasis.opendocument.spreadsheet"}
        odp = {"odp": "application/vnd.oasis.opendocument.presentation"}
        msdoc = {"doc": "application/msword"}
        msdocx = {"docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
        excel1 = {"xls": "application/vnd.ms-excel"}
        excel2 = {"xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
        text = {"txt": "text/plain"}
        csv = {"csv": "text/csv"}
        png = {"png": "image/png"}
        jpeg = {"jpg": "image/jpeg"}
        tiff = {"tiff": "image/tiff"}
        dwg = {"dwg": "image/vnd.dwg"}
        lyr = {"lyr": "application/octet-stream"}
        mpk = {"mpk": "application/octet-stream"}
        mxd = {"mxd": "application/octet-stream"}

        self.FILE_TYPE_CHOICES = {
            "PDF": pdf,
            "OPEN OFFICE DOC": odt,
            "OPEN OFFICE SHEET": ods,
            "OPEN OFFICE PRESENTATION": odp,
            "MS Word doc": msdoc,
            "MS Word docx": msdocx,
            "TEXT": text,
            "MS Excel xls": excel1,
            "MS Excel xlsx": excel2,
            "CSV Spreadsheet": csv,
            "PNG Image": png,
            "JPEG Image": jpeg,
            "TIFF Image": tiff,
            "AutoCad dwg": dwg,
            "ESRI Layer File": lyr,
            "ESRI Map Package": mpk,
            "ESRI Map Document": mxd
        }

        self.DOC_VIEWER_TYPES = ['docx', 'doc', 'txt']

        self.TABLE_VIEWER_TYPES = ['xls', 'xlsx', 'ods']

        self.IMAGE_VIEWER_TYPES = ['tiff', 'jpg', 'png']

        self.engineering_discipline_choices = engineering_discipline_choices

        self.engineering_sheet_types = engineering_sheet_types

        return


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
    view_name = 'fileApp:engineeringfilemodel-detail'
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
        lookup_field = 'pk'

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
        try:
            file_types = FileTypes()
            file_path = validated_data['file_path']
            if os.path.exists(file_path):
                extension = file_path.split(".")[-1].lower()
                base_name = os.path.basename(file_path)
                file_type = function_definitions.check_file_type(file_types.FILE_TYPE_CHOICES, extension)
                size = function_definitions.convert_size(os.path.getsize(file_path))
                mime = mimetypes.guess_type(file_path)[0]

                if mime is None:
                    # solves bug where file extensions are uppercase
                    for mapping in iter(file_types.FILE_TYPE_CHOICES.values()):
                        if extension in mapping:
                            mime = file_types.FILE_TYPE_CHOICES[file_type][extension]

            else:
                base_name = file_path.split("\\")[-1]
                file_type = base_name.split(".")[-1]
                size = ''
                mime = ''
                validated_data["comment"] = 'eDoc system unable to locate file using the file_path'

            # This is very important, all file_paths will be lower case in this system
            validated_data["file_path"] = file_path.lower()
            validated_data["base_name"] = base_name
            validated_data["file_type"] = file_type
            validated_data["size"] = size
            validated_data["mime"] = mime

            _file = EngineeringFileModel.objects.create(**validated_data)
            _file.save()
            return _file
        except Exception as e:
            print(e)

    def update(self, instance, validated_data):
        instance.file_path = validated_data.get('file_path', instance.file_path)
        if os.path.exists(instance.file_path):
            # These attributes are calculated from the actual file object
            # TODO - utilize the same functions from the buildDocStore here
            base_name = os.path.basename(instance.file_path)
            instance.base_name = base_name
            instance.file_type = base_name.split(".")[-1]
            instance.size = function_definitions.convert_size(os.path.getsize(instance.file_path))
            instance.mime = mimetypes.guess_type(instance.file_path)[0]

        instance.comment = validated_data.get('comment', instance.comment)

        # These variables are brought in from the Access Database of Tiffany
        instance.sheet_type = validated_data.get("sheet_type", instance.sheet_type)
        instance.project_title = validated_data.get("project_title", instance.project_title)
        instance.sheet_description = validated_data.get("sheet_description", instance.sheet_description)
        instance.sheet_title = validated_data.get("sheet_title", instance.sheet_title)
        instance.project_date = validated_data.get("project_date", instance.project_date)
        instance.vendor = validated_data.get("vendor", instance.vendor)
        instance.airport = validated_data.get("airport", instance.airport)
        instance.project_description = validated_data.get("project_description", instance.project_description)
        instance.funding_type = validated_data.get("funding_type", instance.funding_type)
        instance.grant_number = validated_data.get("grant_number", instance.grant_number)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
        return instance
