from rest_framework import serializers
from rest_framework.reverse import reverse
from fileApp.models import GridCell, EngineeringAssignment, EngineeringFileModel, DisciplineModel, SheetTypeModel,\
    DocumentTypeModel
from fileApp.utils import function_definitions, domains
import mimetypes
import os
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import logging

type_domains = domains.FileTypes()

logger = logging.getLogger(__name__)


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
        fields = '__all__'
        # fields = ('pk', 'base_name', 'grid_cells', 'file_type', 'size', 'date_added', 'sheet_title', 'sheet_type',
        #           'project_title', 'project_description', 'project_date', 'sheet_description', 'vendor', 'discipline',
        #           'airport', 'funding_type', 'grant_number', 'file_path')
        depth = 2
        read_only_fields = ('last_edited_date', 'base_name', 'file_type', 'size', 'date_added', 'mime')

    grid_cells = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    new_grid_cells = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    sheet_type = serializers.SlugRelatedField(many=True, required=False, slug_field='name', queryset=SheetTypeModel.objects.all())

    discipline = serializers.SlugRelatedField(many=True, required=False, slug_field='name', queryset=DisciplineModel.objects.all())

    document_type = serializers.SlugRelatedField(many=True, required=False, slug_field='name', queryset=DocumentTypeModel.objects.all())

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
            file_types = type_domains
            file_path = validated_data['file_path']
            extension = file_path.split(".")[-1].lower()
            if os.path.exists(file_path):
                base_name = os.path.basename(file_path)
                file_type = function_definitions.check_file_type(file_types.ALL_FILE_TYPES, extension)
                size = function_definitions.convert_size(os.path.getsize(file_path))
                mime = mimetypes.guess_type(file_path)[0]

                if mime is None:
                    # solves bug where file extensions are uppercase
                    for k, v in iter(file_types.ALL_FILE_TYPES.items()):
                        if extension == k:
                            mime = file_types.file_type_choices[v][k]
                            break

            else:
                base_name = file_path.split("\\")[-1]
                file_type = function_definitions.check_file_type(file_types.ALL_FILE_TYPES, extension)
                size = ''
                mime = ''
                validated_data["comment"] = 'eDoc system unable to locate file using the file_path'

            # This is very important, all file_paths will be lower case in this system
            validated_data["file_path"] = file_path.lower()
            validated_data["base_name"] = base_name
            validated_data["file_type"] = file_type
            validated_data["size"] = size
            validated_data["mime"] = mime

            file = EngineeringFileModel.objects.create(**validated_data)
            return file

        except Exception as e:
            print(e)

    def update(self, instance, validated_data):
        try:
            file_types = type_domains
            instance.file_path = validated_data.get('file_path', instance.file_path)
            if os.path.exists(instance.file_path):
                # These attributes are calculated from the actual file object
                extension = instance.file_path.split(".")[-1].lower()
                base_name = os.path.basename(instance.file_path)
                instance.base_name = base_name
                instance.file_type = function_definitions.check_file_type(file_types.ALL_FILE_TYPES, extension)
                instance.size = function_definitions.convert_size(os.path.getsize(instance.file_path))
                instance.mime = mimetypes.guess_type(instance.file_path)[0]
                if instance.mime is None:
                    # solves bug where file extensions are uppercase
                    for k, v in iter(file_types.ALL_FILE_TYPES.items()):
                        if extension in k:
                            instance.mime = file_types.file_type_choices[v][k]
                            break
            # These are editor tracking fields
            instance.last_edited_date = datetime.today()

            instance.last_edited_user = validated_data.get("user", instance.last_edited_user)
            # These variables are lists from validated data
            disc = validated_data.get('discipline')
            if disc:
                rels = instance.discipline.all()
                if rels:
                    for t in rels:
                        if t not in disc:
                            instance.discipline.remove(t)
                for x in disc:
                    try:
                        d = DisciplineModel.objects.get(name=x)
                        instance.discipline.add(d)
                    except ObjectDoesNotExist as e:
                        logging.error(e)

            doc_type = validated_data.get("document_type")
            if doc_type:
                d = instance.document_type.all()
                if d:
                    for t in d:
                        if t not in doc_type:
                            instance.document_type.remove(t)
                for x in doc_type:
                    try:
                        d = DocumentTypeModel.objects.get(name=x)
                        instance.document_type.add(d)
                    except ObjectDoesNotExist as e:
                        logging.error(e)

            s_type = validated_data.get("sheet_type")
            if s_type:
                t = instance.sheet_type.all()
                if t:
                    for m in t:
                        if m not in s_type:
                            instance.sheet_type.remove(m)

                for x in s_type:
                    try:
                        d = SheetTypeModel.objects.get(name=x)
                        instance.sheet_type.add(d)
                    except ObjectDoesNotExist as e:
                        logging.error(e)

            m_grids = validated_data.get("grid_cells")
            if m_grids:
                g = instance.grid_cells.all()
                if g:
                    for m in g:
                        if m.name not in m_grids:
                            try:
                                target = EngineeringAssignment.objects.get(file=instance, grid_cell=m)
                                target.delete()
                            except ObjectDoesNotExist:
                                pass
            else:
                # remove all assignments if they exist
                target = EngineeringAssignment.objects.filter(file=instance)
                target.delete()

            new_grids = validated_data.get("new_grid_cells")
            if new_grids:
                for x in new_grids:
                    g_cell = GridCell.objects.get(name=x)
                    try:
                        EngineeringAssignment.objects.get(file=instance, grid_cell=g_cell)
                    except ObjectDoesNotExist:
                        EngineeringAssignment.objects.create(file=instance, grid_cell=g_cell)

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
        except Exception as e:
            print(e)
