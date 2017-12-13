import os
import openpyxl
from openpyxl import Workbook
import json

wb = Workbook()

fields = json.loads(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "space_domains.json"), 'r').read())

for f in fields:
    ws = wb.create_sheet(title=f["name"])
    ws.append(["Code", "Description"])
    domain = f["domain"]
    for x in domain["codedValues"]:
        ws.append([x["code"], x["name"]])

wb.save("RTAA_Domain_Sheets.xlsx")