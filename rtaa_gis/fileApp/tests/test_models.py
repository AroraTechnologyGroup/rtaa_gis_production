from django.test import TestCase
from fileApp.models import Assignment, FileModel, GridCell
import os


class TestAssignment(TestCase):
    def setUp(self):
        assign = Assignment.objects.create(
            grid_cell='32',
            file=os.path.abspath(__file__),
            comment="test assignment",
        )
        assign.save()


class TestFileModel(TestCase):
    def setup(self):
        file_path = os.path.abspath(__file__)
        base_name = os.path.basename(file_path)
        file_type = "PDF"
        mime = "application/pdf"
        size = "32 MB"

        file_obj = FileModel.objects.create(
            file_path=file_path,
            base_name=base_name,
            file_type=file_type,
            mime=mime,
            size=size
        )
        file_obj.save()


class TestGridCell(TestCase):
    def setup(self):
        grid_cell = GridCell.objects.create(
            name='32'
        )
        grid_cell.save()
