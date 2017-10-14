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
import xlrd
from arcgis.gis import GIS
import pprint

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rtaa_gis.settings'
django.setup()
import lpm
from lpm import models
from lpm.models import AgreementModel
from lpm.serializers import AgreementSerializer

from django.conf import settings

##############################################
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs/ABM_bridge.txt")
file = open(log_path, 'w')
file.close()


def loggit(text):
    file = open(log_path, 'a')
    file.write("{}\n".format(text))
    pprint.pprint("{}\n".format(text))
    file.close()

###############################################
pkid_leasee = {}

wb = xlrd.open_workbook("PKID_Table.xls")

sheet = wb.sheet_by_index(0)
for rx in range(sheet.nrows):
    _row = sheet.row(rx)
    if _row[2].value != 'pkAgreementID':
        pkid_leasee[int(_row[2].value)] = _row[1].value

kwargs = dict()
kwargs['driver'] = '{SQL Server}'
kwargs['server'] = 'Reno-fis-sql2'
kwargs['database'] = 'ABM_Reno_GIS'

connGIS = pyodbc.connect(**kwargs)

kwargs['database'] = 'ABM_Reno_Prod'
connPROD = pyodbc.connect(**kwargs)


def queryConnection(connection):
    """take in the _mssql connection and write out geometries"""
    # query each connection database
    data = {}
    status_types = {
        "ACTV": "Active",
        "MTM": "Month-to-Month",
        "YTY": "Year-to-Year",
        "PEND": "Pending"
    }
    agreement_types = {}
    cursor = connection.cursor()
    # # get the Agreement Type Descriptions into an object
    cursor.execute("SELECT [pkAgreementTypeID], [AgreementTypeDescription]\
    FROM [ABM_Reno_Prod].[dbo].[trefagTypes]")
    for row in cursor:
        agreement_types[row[0]] = row[1]

    cursor.execute("SELECT [pkAgreementID],\
    [AgreementNumber],[AgreementTitle],\
    [fkAgreementStatusID], [fkAgreementTypeID]\
     FROM [ABM_Reno_Prod].[dbo].[tblagAgreements]\
    WHERE [fkAgreementStatusID] = 'ACTV'")
    for row in cursor:

        if row[3].upper() in status_types.keys():

            data[row[0]] = {
                "AgreementNumber": row[1],
                "AgreementTitle": row[2],
                "AgreementType": agreement_types[row[4]],
                "AgreementStatus": status_types[row[3]]
            }

    ids = data.keys()
    for key in ids:
        cursor.execute("SELECT [fkAgreementID], \
        [fkDateTypeID], [DateValue]\
        FROM [ABM_Reno_Prod].[dbo].[tblagAgreementDates]\
        WHERE [fkAgreementID] = '{}'".format(key))
        for row in cursor:
            try:
                id_int = int(row[0])
                if id_int == key:
                    date_type = row[1]
                    date_value = row[2]
                    if date_type in ["EXEC", "START"]:
                        data[key]["StartDate"] = date_value
                    if date_type in ["END", "EXPIR"]:
                        data[key]["Expiration"] = date_value
                    # if the start date or the end date have not been set, make it Unknown
                    existing_fields = data[key].keys()
                    if "StartDate" not in existing_fields:
                        data[key]["StartDate"] = None
                    if "Expiration" not in existing_fields:
                        data[key]["Expiration"] = None
            except Exception as e:
                loggit(e)

    try:
        # before returning this object, verify every value has each of the time-enabling properties needed
        ids_no_date = []
        for k, v in data.items():
            keys = v.keys()
            fields = ["StartDate", "Expiration"]
            for f in fields:
                if f not in keys:
                    ids_no_date.append(k)
                    data[k][f] = None

        ids_no_date = list(set(ids_no_date))
        if ids_no_date:
            cursor.execute("SELECT [fkAgreementID], \
                   FROM [ABM_Reno_Prod].[dbo].[tblagAgreementDates]")
            for row in cursor:
                if row[0] in ids_no_date:
                    ids_no_date.remove(row[0])
            if ids_no_date:
                loggit("These Agreement IDs were not found in the Date Table :: {}\n".format(ids_no_date))
    except Exception as e:
        loggit("Error when checking object fields")
    return data


if __name__ == "__main__":
    try:
        review_notes = {}
        x = queryConnection(connPROD)
        # check if a leasee has multiple active agreements

        gis = GIS("https://www.arcgis.com", "data_owner", "GIS@RTAA123!")
        lease_spaces = gis.content.get('981a15cb963d496a83efb13b62a71c39')
        # level1_terminal = gis.content.get('2bea9f63c64a4b68b18d021d5553aabf')
        # mini_warehouse = gis.content.get('afe5c07cc78a4d63a39472b5925fe0b2')
        # land_leases = gis.content.get('623e53299c80400b8e560fde4e497ebf')
        # ga_west_box_hangars = gis.content.get('324d3a463f8c434492f128b97ac2fd36')
        # ga_west_t_hangars = gis.content.get('a9672d33b31c4b0bae29f194a84737f0')
        # ga_east_tie_downs = gis.content.get('c966dc6809054b9b9b716cd3f6a65805')
        # ga_east_box_hangars = gis.content.get('15acb05a8d9d4320b30cddd282064adc')
        # ga_east_t_hangars = gis.content.get('ebefc416896a44f3be6bbc3e3c7df552')
        # level2_terminal = gis.content.get('4b8e861cf4a7431b9117bb912156e23e')

        for layer in [lease_spaces]:
            for k, v in pkid_leasee.items():
                # if the pkid from the excel file exists in the active agreements dict
                if k in x:
                    feature_layer = layer.layers[0]
                    feature_set = feature_layer.query(where="TENANT_NAME = '{}'".format(v))
                    if len(feature_set.features):
                        filtered = feature_set.features
                        for lyr in filtered:
                            pkids = []
                            existing_att = lyr.attributes["AGREEMENT_ID"]
                            if existing_att:
                                pkids.extend(existing_att.split(","))

                            pkids.append(str(k))
                            pkids = list(set(pkids))
                            lyr_edit = lyr
                            if len(pkids) > 1:
                                if v in review_notes:
                                    if k not in review_notes[v]:
                                        review_notes[v].append(k)
                                else:
                                    review_notes[v] = [k]

                            elif len(pkids) == 1:
                                lyr_edit.attributes["AGREEMENT_TYPE"] = x[k]["AgreementType"]
                                lyr_edit.attributes["START_DATE"] = x[k]["StartDate"]
                                lyr_edit.attributes["EXPIRATION"] = x[k]["Expiration"]

                            lyr_edit.attributes["AGREEMENT_ID"] = ",".join(pkids)
                            try:
                                update_result = feature_layer.edit_features(updates=[lyr_edit])
                            except RuntimeError as Exception:
                                loggit(Exception)
        loggit("Review Notes: {}".format(review_notes))
    except:
        traceback.print_exc(file=sys.stdout)

