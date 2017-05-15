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
from fileApp.serializers import EngSerializer
from fileApp.models import EngineeringFileModel, EngineeringDiscipline, EngineeringSheetType, GridCell
from fileApp.utils import function_definitions
fixtures_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures\\data')
TOP_DIRs = [fixtures_path]


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
                r'DBQ=%s;' % os.path.join(fixtures_path, 'reno.accdb')
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

                    if row[-1] != 'text':
                        if len(filtered) == 0:
                            new_obj = {
                                'file_path': file_path,
                                'sheet_type': [],
                                'discipline': [],
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
                                # add the relationships tables
                                _obj = EngineeringFileModel.objects.get(file_path=file_path)
                                if discipline:
                                    # using the disciplines defined in the model
                                    disc_upper = discipline.upper()
                                    discs = []
                                    for x in models.engineering_sheet_types:
                                        pass
                                    discs = EngineeringDiscipline.objects.get(name=disc_upper)
                                    _obj.discipline.add(discs)
                                if sheet_type:
                                    stypes = EngineeringSheetType.objects.get(name=sheet_type)
                                    _obj.sheet_type.add(stypes)

                            else:
                                print(ser_obj.errors)
                        elif len(filtered) == 1:
                            _object = filtered[0]
                            serializer = EngSerializer(_object)
                            new_data = {}

                            if sheet_type:
                                sh = sheet_type.upper()
                                stypes = []
                                for x in models.engineering_sheet_types:
                                    if x[0] in sh:
                                        stypes.append(x[0])
                                stypes = EngineeringSheetType.objects.filter(name__in=stypes)
                                for t in stypes:
                                    _object.sheet_type.add(t)

                            if discipline:
                                disc = discipline.upper()
                                discs = []
                                for x in models.engineering_discipline_choices:
                                    if x[0] in disc:
                                        discs.append(x[0])
                                discs = EngineeringDiscipline.objects.filter(name__in=discs)
                                for d in discs:
                                    _object.discipline.add(d)

                            new_data["file_path"] = file_path
                            new_data["project_title"] = project_title
                            new_data["sheet_description"] = sheet_description
                            new_data["sheet_title"] = sheet_title
                            new_data["project_date"] = project_date,
                            new_data["vendor"] = vendor
                            new_data["airport"] = ''
                            new_data["project_description"] = ''
                            new_data["funding_type"] = ''
                            new_data["grant_number"] = ''

                            try:
                                new_s = EngSerializer(data=new_data)
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
                            # if the extension is IN the dict as a value is good enough
                            if extension in mapping:
                                file_path = os.path.join(root, _file)
                                base_name = os.path.basename(file_path)
                                file_type = function_definitions.check_file_type(FILE_TYPE_CHOICES, extension)[0]
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
        remove paths that don't match with TOP_DIRs;"""
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
        # send query request to esri rest api
        login_params = {
            'f': 'json',
            'client_id': 'Yer7Ki5IEHLbDzqv',
            'client_secret': 'a6b5f07dbd6d4228a0cb334cdad8d575',
            'grant_type': 'client_credentials',
            'expiration': '1440',
        }

        token = requests.post('https://www.arcgis.com/sharing/rest/oauth2/token/',
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


if __name__ == '__main__':
    x = FileStoreBuilder()
    x.load_accdb()