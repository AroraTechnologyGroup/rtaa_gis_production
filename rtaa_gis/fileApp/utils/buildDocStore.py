import os
import mimetypes
import sys
import django
import requests
import logging
import json
import traceback
import pyodbc
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rtaa_gis.settings'
django.setup()
from fileApp import models
from fileApp.models import EngineeringFileModel, EngineeringAssignment, GridCell
from fileApp.serializers import EngSerializer, EngAssignmentSerializer, engineering_sheet_types, engineering_discipline_choices
from fileApp.utils import function_definitions
from django.conf import settings

TOP_DIRs = settings.FILE_APP_TOP_DIRS
acc_db_path = ""
# for testing load the sample pdf files
# test_dir = os.path.join(settings.BASE_DIR, "fileApp/fixtures/data")
# TOP_DIRs = [test_dir]
# acc_db_path = test_dir

PDF = {"pdf": "application/pdf"}
ODT = {"odt": "application/vnd.oasis.opendocument.text"}
ODS = {"ods": "application/vnd.oasis.opendocument.spreadsheet"}
ODP = {"odp": "application/vnd.oasis.opendocument.presentation"}
MSDOC = {"doc": "application/msword"}
MSDOCX = {"docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
EXCEL1 = {"xls": "application/vnd.ms-excel"}
EXCEL2 = {"xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}
TEXT = {"txt": "text/plain"}
CSV = {"csv": "text/csv"}
PNG = {"png": "image/png"}
JPEG = {"jpg": "image/jpeg"}
TIFF = {"tiff": "image/tiff"}
DWG = {"dwg": "image/vnd.dwg"}
LYR = {"lyr": "application/octet-stream"}
MPK = {"mpk": "application/octet-stream"}
MXD = {"mxd": "application/octet-stream"}

FILE_TYPE_CHOICES = {
    "PDF": PDF,
    "OPEN OFFICE DOC": ODT,
    "OPEN OFFICE SHEET": ODS,
    "OPEN OFFICE PRESENTATION": ODP,
    "MS Word doc": MSDOC,
    "MS Word docx": MSDOCX,
    "TEXT": TEXT,
    "MS Excel xls": EXCEL1,
    "MS Excel xlsx": EXCEL2,
    "CSV Spreadsheet": CSV,
    "PNG Image": PNG,
    "JPEG Image": JPEG,
    "TIFF Image": TIFF,
    "AutoCad dwg": DWG,
    "ESRI Layer File": LYR,
    "ESRI Map Package": MPK,
    "ESRI Map Document": MXD
}

DOC_VIEWER_TYPES = ['docx', 'doc', 'txt']

TABLE_VIEWER_TYPES = ['xls', 'xlsx', 'ods']

IMAGE_VIEWER_TYPES = ['tiff', 'jpg', 'png']


def __init__(self):
    self.FILE_TYPE_CHOICES = FILE_TYPE_CHOICES
    self.TOP_DIRs = TOP_DIRs
    return


class Error(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FileStoreBuilder:
    def __init__(self):
        self.top_dirs = TOP_DIRs
        pass

    def load_accdb(self):
        try:
            conn_str = (
                r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
                r'DBQ=%s;' % os.path.join(acc_db_path, 'reno.accdb')
            )
            cnxn = pyodbc.connect(conn_str)
            cursor = cnxn.cursor()
            cursor.execute("SELECT FILENAME, SHEETTYPE, DISCIPLINE, PROJECTNAME, SHEETDESCRIPTION,"
                           "SHEETNUMBER, DATE, VENDOR FROM reno")
            rows = cursor.fetchall()
            for row in rows:
                if row[-1] != 'text':
                    file_path, sheet_type, discipline, project_title, sheet_description, sheet_title, project_date, vendor = row
                    file_path = file_path.replace('#', '')
                    if not file_path:
                        file_path = ""
                    filtered = EngineeringFileModel.objects.filter(file_path=file_path)
                    if not vendor:
                        vendor = ""
                    if project_date:
                        project_date = datetime.date(int(project_date), 1, 1)
                    if not project_date:
                        project_date = datetime.date(9999, 1, 1)
                    if not sheet_title:
                        sheet_title = ""
                    if not sheet_type:
                        sheet_type = ""
                    if not discipline:
                        discipline = ""
                    if not project_title:
                        project_title = ""
                    if not sheet_description:
                        sheet_description = ""

                    if len(filtered) == 0:
                        new_obj = {
                            'file_path': file_path,
                            'sheet_type': sheet_type,
                            'discipline': discipline,
                            'project_title': project_title,
                            'sheet_description': sheet_description,
                            'sheet_title': sheet_title,
                            'project_date': project_date,
                            'vendor': vendor,
                            'airport': '',
                            'project_description': '',
                            'funding_type': '',
                            'grant_number': ''
                        }
                        ser_obj = EngSerializer(data=new_obj)
                        if ser_obj.is_valid():
                            ser_obj.save()
                        else:
                            print(ser_obj.errors)

                    elif len(filtered) == 1:
                        _object = filtered[0]
                        serializer = EngSerializer(_object)
                        update_data = {
                            "file_path": file_path,
                            "sheet_type": sheet_type,
                            "project_title": project_title,
                            "sheet_description": sheet_description,
                            "sheet_title": sheet_title,
                            "project_date": project_date,
                            "vendor": vendor,
                            "airport": '',
                            "project_description": '',
                            "funding_type": '',
                            "grant_number": ''
                        }

                        try:
                            new_s = EngSerializer(data=update_data)
                            if new_s.is_valid():
                                serializer.update(new_s.data)
                            else:
                                print(new_s.errors)
                        except:
                            exc_type, exc_value, exc_traceback = sys.exc_info()
                            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

    def build_store(self):
        try:
            top_dirs = self.top_dirs
            for top_dir in top_dirs:
                for root, dirs, files in os.walk(top_dir):
                    for _file in files:
                        # solves bug where file extensions are uppercase
                        extension = _file.split(".")[-1].lower()
                        for mapping in iter(FILE_TYPE_CHOICES.values()):
                            # there is only one key for each mapping dict so testing
                            # if the extension is IN the dict as a key is good enough
                            if extension in mapping:
                                file_path = os.path.join(root, _file)
                                file_path = file_path.replace("\\", "/")
                                base_name = os.path.basename(file_path)
                                file_type = function_definitions.check_file_type(FILE_TYPE_CHOICES, extension)
                                mime = mimetypes.guess_type(file_path)[0]
                                if mime is None:
                                    mime = FILE_TYPE_CHOICES[file_type][extension]
                                    # print mime
                                size = function_definitions.convert_size(os.path.getsize(file_path))

                                filtered = EngineeringFileModel.objects.filter(file_path=file_path)
                                if len(filtered) == 0:
                                    # File has not been added to the database
                                    new_obj = EngineeringFileModel.objects.create(
                                            file_path=file_path,
                                            base_name=base_name,
                                            file_type=file_type,
                                            mime=mime,
                                            size=size
                                    )
                                    new_obj.save()

                                elif len(filtered) == 1:
                                    # The File Exists in the Database and will be updated
                                    _object = filtered[0]
                                    _object.file_path = file_path
                                    _object.base_name = base_name
                                    _object.file_type = file_type
                                    _object.mime = mime
                                    _object.size = size
                                    _object.save()

        except Exception as e:
            logging.warning(e)

        return

    def clean_store(self):
        """Remove paths that don't exist;
        Remove directories;
        remove paths that don't match with TOP_DIRs;
       """
        def check_roots(in_path, roots):
            d = False
            for x in roots:
                d = d
                if in_path.startswith(x):
                    if os.path.exists(in_path):
                        if not os.path.isdir(in_path):
                            d = True
            return d

        try:
            file_paths = []
            for _file in EngineeringFileModel.objects.all():
                path = _file.file_path
                if not check_roots(path, self.top_dirs):
                    _file.delete()

                else:
                    if path not in file_paths:
                        file_paths.append(path)
                    else:
                        raise Error("Duplicate file objects with path {}".format(path))
                        # TODO - if two files are the same path, merge their grid cell assignments
                        pass

        except Exception as e:
            print(e)


class GridCellBuilder:
    def __init__(self):
        pass

    @staticmethod
    def build_store():
        """This will create new grid cell rows only if they dont exist"""
        # send query request to esri rest api
        login_params = {
            'client_id': 'iVMcOt2MrFfgmRBF',
            'client_secret': 'e6df1381878a49e8b3df8e5c654c0110',
            'grant_type': 'client_credentials'
        }

        token = requests.get('https://www.arcgis.com/sharing/rest/oauth2/token/',
                              params=login_params)
        access_token = token.json()['access_token']

        query_url = r'https://services1.arcgis.com/Apy6bpbM5OoW9DX4/arcgis/rest/services/MapGrid_StatePlane/FeatureServer/0/query'
        query_params = {
            'f': 'json',
            'token': access_token,
            'returnM': 'false',
            'returnZ': 'false',
            'returnDistinctValues': 'true',
            'returnGeometry': 'false',
            'outFields': 'GRID',
            'where': "Id LIKE '%'"
        }

        feature_service = requests.post(query_url, params=query_params)

        features = feature_service.json()['features']
        for feature in features:

            grid = feature['attributes']['GRID']
            name = '{}'.format(grid)
            try:
                filtered = GridCell.objects.filter(name=name)
                # Only create a document if one with that name does not exist
                if len(filtered) == 0:
                    x = GridCell.objects.create(name=name)
                    x.save()
                else:
                    pass

            except Exception as e:
                logging.error("Error populating the Grid Model {}".format(name))
                print(e)


class AssignmentManager:
    def __init__(self):
        pass

    def clear(self, data):
        pass

    @staticmethod
    def create_test_assignments():
        files = EngineeringFileModel.objects.all()
        grid_cells = GridCell.objects.all()
        i = 0
        for file in files:
            try:
                grid_cell = grid_cells[i]
                new_obj = {
                    "file": "http://127.0.0.1:8080/fileApp/eng-files/{}/".format(file.pk),
                    "grid_cell": grid_cell.name
                }
                i += 3

                try:
                    existing = EngineeringAssignment.objects.filter(grid_cell=grid_cell).filter(file=file)
                    if len(existing):
                        check = EngAssignmentSerializer(existing[0], data=new_obj)
                    else:
                        check = EngAssignmentSerializer(data=new_obj)

                    if check.is_valid():
                        check.save()

                    else:
                        print("{} and {} could not be assigned".format(grid_cell, file.base_name))
                except Exception:
                    print(Exception)

            except IndexError:
                pass


if __name__ == '__main__':
    x = FileStoreBuilder()
    x.build_store()
    cell = GridCellBuilder()
    cell.build_store()
    ass = AssignmentManager()
    ass.create_test_assignments()

