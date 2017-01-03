import sys
import os
import django
from openpyxl import Workbook

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rtaa_gis.settings'
django.setup()
from rtaa_gis.settings import MEDIA_ROOT

from cloudSync.models import FeatureClass

outfile = os.path.join(MEDIA_ROOT, "fclass_report.xlsx")
wb = Workbook()

ws = wb.active

headings = ["Select", "Feature Class Name", "Number of Features"]
ws.append(headings)

fcs = FeatureClass.objects.all()
for fc in fcs:
    ws.append(["", fc.baseName, fc.count])

wb.save(outfile)

