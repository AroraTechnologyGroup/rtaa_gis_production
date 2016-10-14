from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import FileModel, GridCell, Assignment
from .utils import buildDocStore
import mimetypes
import os


class FileSerializer(serializers.ModelSerializer):

    grid_cells = serializers.SerializerMethodField()

    class Meta:
        model = FileModel
        fields = ('pk', 'file_path', 'base_name', 'grid_cells', 'file_type', 'size', 'date_added', 'mime',
                  'comment')
        depth = 1
        read_only_fields = ('pk', 'base_name', 'grid_cells', 'file_type', 'size', 'date_added', 'mime')

    @staticmethod
    def get_grid_cells(self):
        base_name = self.base_name
        file_path = self.file_path
        assigns = Assignment.objects.filter(base_name=base_name)
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
        base_name = os.path.basename(file_path)
        file_type = base_name.split(".")[-1]
        size = buildDocStore.convert_size(os.path.getsize(file_path))
        mime = mimetypes.guess_type(file_path)[0]
        if mime is None:
            mime = "UNK"
        comment = validated_data['comment']

        _file = FileModel.objects.create(
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
        base_name = os.path.basename(file_path)

        instance.file_path = file_path
        instance.base_name = base_name
        instance.file_type = base_name.split(".")[-1]
        instance.size = buildDocStore.convert_size(os.path.getsize(file_path))
        instance.mime = mimetypes.guess_type(file_path)[0]

        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class GridSerializer(serializers.ModelSerializer):

    class Meta:
        model = GridCell
        fields = ('name',)
        read_only_fields = ('name',)

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class FileHyperLinkedRelatedField(serializers.HyperlinkedRelatedField):
    queryset = FileModel.objects.all()
    view_name = 'filemodel-detail'
    lookup_field = 'pk'
    many = False

    def display_value(self, instance):
        return instance.file_path


class GridPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    queryset = GridCell.objects.all()
    many = False
    pk_field = 'Name'

    def display_value(self, instance):
        return '%s' % instance.name


class AssignmentSerializer(serializers.ModelSerializer):

    grid_cell = GridPrimaryKeyRelatedField()

    file = FileHyperLinkedRelatedField()

    class Meta:
        model = Assignment
        fields = ('pk', 'grid_cell', 'file', 'base_name', 'comment', 'date_assigned')
        depth = 1
        read_only_fields = ('base_name', 'date_assigned')

    def create(self, validated_data):
        base_name = validated_data['file'].base_name

        assignment = Assignment.objects.create(base_name=base_name, **validated_data)
        assignment.save()
        return assignment

    def update(self, instance, validated_data):
        instance.grid_cell = validated_data.get('grid_cell', instance.grid_cell)
        instance.file = validated_data.get('file', instance.file)
        instance.base_name = os.path.basename(instance.file.file_path)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance
