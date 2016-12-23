#! C:\Python27\ArcGIS10.4\python.exe

import arcpy
from arcpy import env
from arcpy import da
import time
import os
from arcpy import mapping
from collections import Counter


env.overwriteOutput = 1
path = os.path.abspath(os.path.dirname(__file__))
print(path)
os.chdir(path)
print(os.getcwd())

# Location of Geodatabase
##demodata = arcpy.GetParameterAsText(0)
demodata = r"C:\ESRI_WORK_FOLDER\rtaa\RNO_Master_GDB.gdb"
desc = arcpy.Describe(demodata)
basename = desc.basename
env.workspace = demodata


def createHTML(htmlfile):
    path = arcpy.Describe(demodata).path
    filename = "{}\\{}.html".format(path, htmlfile)
    html = open(filename, "w")
    html.write("""<!DOCTYPE html>

    <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta charset="utf-8" />
        <title>Describing %s for Review</title>
        <style>
            td {
                text-align: center;
                padding: 10px;
                border-right: 1px dashed black;
            }

            tr {
                display: table-row-group;
                border-bottom: 1px solid black;

            }

            tbody {
                display:table;
                border-collapse:collapse;
            }

            .maintable {
                display: none;
                border-collapse: collapse;
                overflow: scroll;
                margin-left: 5px;
                margin-right: auto;
                border: 2px solid black;
            }

            .maintable th{
                border-right: 1px dashed black;
                padding: 5px;
                font-size: large;
            }

            .maintable td {
                font-size: small;
            }

            .rowtable  {
                display: table;
                margin-left: auto;
                margin-right: auto;
            }

            .rowtable th{
                border:none;
            }

            .rowtable  td{
                text-align: justify;
                border: 1px solid black;
            }

            .dataset {
                display: none;
                border-collapse:collapse;
                overflow: scroll;
                margin-left: 5px;
                margin-right: auto;
                border: 2px solid black;
            }

            .dataset th {
                border-right: 1px dashed black;
                padding: 5px;
                font-size: large;
            }

            .dataset td {
                font-size: small;
            }

            .fctable {
                border-collapse: collapse;
                display:none;
                padding: 0px;
                margin-left: 5px;
                margin-bottom: 5px;
                border: 2px solid black;
            }

            .fieldtable {
                border-collapse: collapse;
                display:none;
                border-right: 1px solid black;
            }

            .fieldtable th {
                font-size: large;
                border-top: 1px solid black;
                border-left: 1px solid black;
            }

            .fieldtable td {
                font-size: small;
                background-color: WindowFrame;
                border: 1px solid black;
            }

            button {
                padding: 5px;
                margin:5px;

            }

            fc_buttons {
                display: none;
            }
        </style>
        <script>
            function changetable(id) {
                var el = document.getElementById(id)
                if (el.style.display === 'none') {
                    el.style.display = 'table'
                } else {el.style.display = 'none'};
                return
            };
        </script>
    </head>"""% htmlfile.split("\\")[-1].rstrip(".html"))
    html.close()

def logging(htmlfile, text):
    filename = "{}\\{}.html".format(path, htmlfile)
    html = open(filename, "a")
    html.write("{} \n".format(text))
    html.close()

htmlfile = "Domains"
createHTML(htmlfile)
logging(htmlfile, """<body>
                <button onclick='changetable("domains")';>DOMAINS inside of geodatabase {}</button>
                    <table class='maintable' id='domains'>
                    <tbody>
                        <tr>
                            <th data-sort='name'><b>Domain Name</b></th>
                            <th data-sort='field_type'><b>FIELD Type</b></th>
                            <th data-sort='domain_type'><b>Domain Type</b></th>
                            <th><b>Domain Values/Range</b></th>
                        </tr>""".format(basename))


# Print version of ArcGIS available
x = arcpy.GetInstallInfo()["Version"]
print(x)
if x in ['9.2', '9.3', '10.0', '10.1']:
    print("Table to Excel not supported")
    version = 0
else:
    print("Table to Excel is supported")
    version = 1

# #################################################################################################


domains = arcpy.da.ListDomains(demodata)
for domain in domains:
    print(domain.name)
    x = domain.domainType
    if x == "CodedValue":
        print(domain.codedValues)
    elif x == "Range":
        print(domain.range)
    print("field type :: {}".format(domain.type))
    # print("Merge Policy :: {}".format(domain.MergePolicy))
    # print("SplitPolicy :: {}".format(domain.SplitPolicy))
for domain in domains:
    x = domain.domainType
    if x == "CodedValue":
        cvalues = domain.codedValues
        logging(htmlfile, """ <tr>
                    <td>{0}</td>
                    <td>{1}</td>
                    <td>{2}</td>
                    <td>
                        <table class='rowtable'>
                        <tbody>
                            <tr><th>Code</th><th>Value</th></tr>
                            """.format(domain.name, domain.type, x))
        for val in cvalues:
            logging(htmlfile, """         <tr>
                                <td>{}</td>
                                <td>{}</td>
                                </tr>""".format(val, cvalues[val]))
                                    
        logging(htmlfile, """     </tbody>
                        </table>
                    </td>
                    </tr>""")
       
    elif x == "Range":
        logging(htmlfile, """<tr>
                    <td>{0}</td>
                    <td>{1}</td>
                    <td>{2}</td>
                    <td>{3}</td>
                    </tr>""".format(domain.name, domain.type, x, domain.range))
logging(htmlfile, """ </tbody>
            </table>
        </html>""")

datasets = arcpy.ListDatasets()
try:
    if len(datasets):
        for dataset in datasets:
            htmlfile = "{}".format(dataset)
            createHTML(htmlfile)
            
            env.workspace = "{}\\{}".format(demodata, dataset)
            click = dataset
           
            logging(htmlfile, """<button type='button' style='display:block' onclick='changetable("datasets")';>DATASETS inside of geodatabase {}</button>
                        <table class='dataset' id='datasets'>
                            <tbody>
                            <tr>
                                <th data-sort='name'><b>DATASET NAME</b></th>
                                <th data-sort='field_type'><b>SPATIAL REFERENCE</b></th>
                                <th data-sort='dataset_type'><b>DATASET TYPE</b></th>
                                <th><b>X-Max EXTENT of DATASET</b></th>
                                <th><b>X-Min EXTENT of DATASET</b></th>
                                <th><b>Y-Max EXTENT of DATASET</b></th>
                                <th><b>Y-Min EXTENT of DATASET</b></th>
                            </tr>""".format(basename))


            descdata = arcpy.Describe("{}\\{}".format(demodata, dataset))
            logging(htmlfile, """ <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>
                        <td>{}</td></tr>""".format(
                dataset, descdata.spatialReference.name, descdata.datasetType, descdata.extent.XMax, descdata.extent.XMin,
                descdata.extent.YMax, descdata.extent.YMin))

            # List feature classes inside dataset and add a field for each one
            fclist = arcpy.ListFeatureClasses()

            logging(htmlfile, """<tr><td>
                    <button type='button' onclick='changetable("{0}")';>--Dataset {0}: Feature Classes</button>
                    </td></tr>
                    <tr><td>
                        <table class='fctable' id='{0}'>
                            <tbody>
                                <tr>
                                    <th data-sort='name'><b>FEATURE CLASS NAME</b></th>
                                    <th><b>Feature Type</b></th>
                                    <th><b>Number of Features</b></th>
                                    <th><b>Has M Values?</b></th>
                                    <th><b>Has Z Values?</b></th>
                                    <th><b>Has Spatial Index?</b></th>
                                    <th><b>Type of Geometry</b>
                                </tr> """.format(dataset))
            if len(fclist) > 0:
                fclist.sort()
                for fc in fclist:
                    descfc = arcpy.Describe(fc)
                    count = int(arcpy.GetCount_management(fc).getOutput(0))
                    logging(htmlfile, """ <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(
                        fc, descfc.featureType, count, descfc.hasM, descfc.hasZ, descfc.hasSpatialIndex, descfc.shapeType))

                    fields = arcpy.ListFields(fc)

                    logging(htmlfile, """ <tr><td>
                                <button type='button' onclick='changetable("{0}")';>{0}: Fields</button>
                                </td></tr>
                                <tr><td>
                                    <table class='fieldtable' id='{0}'>
                                    <tbody>
                                        <tr>
                                            <th data-sort='name'><b>FIELD NAME</b></th>
                                            <th><b>FIELD ALIAS</b></th>
                                            <th><b>FIELD DOMAIN</b></th>
                                            <th><b>FIELD Editable?</b></th>
                                            <th><b>FIELD NULLABLE?</b></th>
                                            <th><b>FIELD LENGTH</b></th>
                                            <th><b>FIELD PRECISION</b></th>
                                            <th><b>FIELD REQUIRED?</b></th>
                                            <th><b>FIELD SCALE</b></th>
                                            <th><b>FIELD TYPE</b></th>
                                            <th><b>Counts of Attribute Values</b></th>
                                            <th><b>FLAG for REMOVAL</b></th>
                                            <th><b>Percent Populated</b></th>
                                        </tr>""".format(fc))

                    keeplist = []
                    droplist = []
                    for field in fields:
                        if field.type.upper() not in ["BLOB", "GEOMETRY", "OID", "GUID"] and field.name.upper() not in ["SHAPE_LENGTH", "SHAPE", "GUID"]:
                            keeplist.append(field)
                        else: 
                            droplist.append(field)
                            
                        print(field.name)
                        attributes = []
                        summary = []
                        counts = []
                        if field in keeplist:
                            fcount = int(arcpy.GetCount_management(fc).getOutput(0))

                            if fcount > 0:
                                with da.SearchCursor(fc, field.name) as cursor:
                                    for row in cursor:
                                        attributes.append(str(row[0]))

                                c = Counter(attributes)
                                counts = c.items()
                                print(counts)

                                i = 0
                                for value in attributes:
                                    try:
                                        D = float(value)
                                        D = int(D)
                                    except:
                                        D = value

                                    if str(D) not in ['', ' ', '0', 'None', '<Null>']:
                                        i += 1
  
                                percent = float(i)/fcount * 100.00
                                percent = "%.2f" % percent

                                print("i / fcount = {}".format(percent))
                                if float(percent) < 75:
                                    droplist.append(field)
                                    keeplist.remove(field)
                            else:
                                summary.append("No attributes were found for field {}".format(field.name))
                                droplist.append(field)
                                keeplist.remove(field)
                                percent = 0.0

                        elif field in droplist:
                            percent = 0.0
                        if field in droplist and field not in keeplist:
                            flag = "drop"
                        elif field in keeplist and field not in droplist:
                            flag = "pass"
                        elif field in keeplist and field in droplist:
                            flag = "error, in both lists"

                        if field.type.upper() not in ["BLOB", "GEOMETRY", "OID", "GUID"] and field.name.upper() not in ["SHAPE_LENGTH",  "SHAPE_AREA", "SHAPE", "GUID"]:
                            logging(htmlfile, """    <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>
                            <td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(
                                field.name, field.aliasName, field.domain, field.editable, field.isNullable,
                                field.length, field.precision, field.required, field.scale, field.type, counts, flag, percent))

                    logging(htmlfile, """ </td></tr>
                                </tbody>
                                </table>""")

                logging(htmlfile, """ </td></tr>
                            </tbody>
                            </table>
                            </html>""")
            else:
                logging(htmlfile, """ </td></tr>
                            </tbody>
                            </table>
                            </html>""")
    
    # **Describe Feature Classes inside of Geodatabase Workspace NOT in datasets**#
    env.workspace = demodata
    fclist = arcpy.ListFeatureClasses()
    if len(fclist) > 0:
        htmlfile = "feature_classes"
        createHTML(htmlfile)
        fclist.sort()
        logging(htmlfile, """<body>
                    <button type='button' onclick='changetable("fctable")';>FEATURE CLASSES <b>NOT</b> IN a Dataset</button>
                    <table class='fctable' id='fctable'>
                    <tbody>
                        <tr>
                            <th data-sort='name'><b>FEATURE CLASS NAME</b></th>
                            <th><b>Feature Type</b></th>
                            <th><b>Number of Features</b></th>
                            <th><b>Has M Values?</b></th>
                            <th><b>Has Z Values?</b></th>
                            <th><b>Has Spatial Index?</b></th>
                            <th><b>Type of Geometry</b>
                        </tr>""")

        for fc in fclist:
            env.workspace = "{}".format(demodata)
            descfc = arcpy.Describe(fc)
            count = int(arcpy.GetCount_management(fc).getOutput(0))
            logging(htmlfile, """<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(
                fc, descfc.featureType, count, descfc.hasM, descfc.hasZ, descfc.hasSpatialIndex, descfc.shapeType))

            fields = arcpy.ListFields(fc)

            logging(htmlfile, """<tr><td>
                    <button type='button' onclick='changetable("{0}")';>--Feature Class {0}: Fields
                    </button></td></tr>
                    <tr><td>
                    <table class='fieldtable' id='{0}'>
                    <tbody>
                    <tr>
                        <th data-sort='name'><b>FIELD NAME</b></th>
                        <th><b>FIELD ALIAS</b></th>
                        <th><b>FIELD DOMAIN</b></th>
                        <th><b>FIELD Editable?</b></th>
                        <th><b>FIELD NULLABLE?</b></th>
                        <th><b>FIELD LENGTH</b></th>
                        <th><b>FIELD PRECISION</b></th>
                        <th><b>FIELD REQUIRED?</b></th>
                        <th><b>FIELD SCALE</b></th>
                        <th><b>FIELD TYPE</b></th>
                        <th><b>Counts of Attribute Values</b></th>
                        <th><b>FLAG for REMOVAL</b></th>
                        <th><b>Percent Populated</b></th>
                    </tr>""".format(fc))

            keeplist = []
            droplist = []
            for field in fields:
                if field.type.upper() not in ["BLOB", "GEOMETRY", "OID", "GUID"] and field.name.upper() not in ["SHAPE_LENGTH",  "SHAPE_AREA", "SHAPE", "GUID"]:
                    keeplist.append(field)
                else: 
                    droplist.append(field)
                            
                print(field.name)
                attributes = []
                summary = []
                counts = []
                if field in keeplist:
                    fcount = int(arcpy.GetCount_management(fc).getOutput(0))

                    if fcount > 0:
                        with da.SearchCursor(fc, field.name) as cursor:
                            for row in cursor:
                                attributes.append(str(row[0]))

                        c = Counter(attributes)
                        counts = c.items()
                        print(counts)

                        i = 0
                        for value in attributes:
                            try:
                                D = float(value)
                                D = int(D)
                            except:
                                D = value

                            if str(D) not in ['', ' ', '0', 'None', '<Null>']:
                                i += 1
                        percent = float(i)/fcount * 100.00
                        percent = "%.2f" % percent

                        print("i / fcount = {}".format(percent))
                        if float(percent) < 75:
                            droplist.append(field)
                            keeplist.remove(field)
                    else:
                        summary.append("No attributes were found for field {}".format(field.name))
                        droplist.append(u'{}'.format(field))
                        keeplist.remove(u'{}'.format(field))
                        percent = 0.0
                elif field in droplist:
                    percent = 0.0

                if field in droplist and field not in keeplist:
                    flag = "drop"
                elif field in keeplist and field not in droplist:
                    flag = "pass"
                elif field in keeplist and field in droplist:
                    flag = "error, in both the keeplist and the droplist"

                if field.type.upper() not in ["BLOB", "GEOMETRY", "OID", "GUID"] and field.name.upper() not in ["SHAPE_LENGTH",  "SHAPE_AREA", "SHAPE", "GUID"]:
                    logging(htmlfile, """<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td>
                            <td>{5}</td><td>{6}</td><td>{7}</td><td>{8}</td><td>{9}</td><td>{10}</td><td>{11}</td><td>{12}</td></tr>""".format(
                        field.name, field.aliasName, field.domain, field.editable, field.isNullable,
                        field.length, field.precision, field.required, field.scale, field.type, counts, flag, percent))

            logging(htmlfile, """ </tbody>
                        </table>
                    </html>""")

    # **List Tables inside of Geodatabase Workspace**#
    env.workspace = demodata
    tables = arcpy.ListTables()
    if len(tables) > 0:
        tables.sort()
        htmlfile = "tables"
        createHTML(htmlfile)
        logging(htmlfile, """<body>
                <button type='button' onclick='changetable("tables")';>TABLES IN geodatabase {}</button>
                    <table class='maintable' id='tables'>
                    <tbody>
                        <tr>
                            <th data-sort='name'><b>TABLE NAME</b></th>
                            <td><b>Number of Rows</b></th>
                            <th><b>does table have OID?</b></th>
                            <th><b>name of OID field</b></th>
                        </tr>""".format(demodata))

        for table in tables:
            desc = arcpy.Describe(table)
            count = int(arcpy.GetCount_management(table).getOutput(0))
            logging(htmlfile, """ <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(table, count, desc.hasOID, desc.OIDFieldName))


            fields = arcpy.ListFields(table)
            keeplist = []
            droplist = []
            
            logging(htmlfile, """<tr><td>
                    <button type='button' onclick='changetable("{0}_fields")';>--Table {0}: Fields
                    </button></td></tr>
                    <tr><td>
                    <table class='fieldtable' id='{0}_fields'>
                    <tbody>
                        <tr>
                            <th data-sort='name'><b>FIELD NAME</b></th>
                            <th><b>FIELD ALIAS</b></th>
                            <th><b>FIELD DOMAIN</b></th>
                            <th><b>FIELD Editable?</b></th>
                            <th><b>FIELD NULLABLE?</b></th>
                            <th><b>FIELD LENGTH</b></th>
                            <th><b>FIELD PRECISION</b></th>
                            <th><b>FIELD REQUIRED?</b></th>
                            <th><b>FIELD SCALE</b></th>
                            <th><b>FIELD TYPE</b></th>
                            <th><b>(Attribute, number of occurances)</b></th>
                            <th><b>Flag for Removal</b></th>
                            <th><b>Percent Populated</b></th>
                        </tr>""".format(table))
            for field in fields:
                if field.type.upper() not in ["BLOB", "GEOMETRY", "OID", "GUID"] and field.name.upper() not in ["SHAPE_LENGTH",  "SHAPE_AREA", "SHAPE", "GUID"]:
                    keeplist.append(field)
                else: 
                    droplist.append(field)
                            
                print(field.name)
                attributes = []
                summary = []
                counts = []
                if field in keeplist:
                    fcount = int(arcpy.GetCount_management(table).getOutput(0))

                    if fcount > 0:
                        with da.SearchCursor(table, field.name) as cursor:
                            for row in cursor:
                                attributes.append(str(row[0]))

                        c = Counter(attributes)
                        counts = c.items()
                        print(counts)

                        i = 0
                        for value in attributes:
                            print(c)
                            try:
                                D = float(value)
                                D = int(D)
                            except:
                                D = value

                            if str(D) not in ['', ' ', '0', 'None', '<Null>']:
                                i += 1

                        percent = float(i)/fcount * 100.00
                        percent = "%.2f" % percent

                        print("i / fcount = {}".format(percent))
                        if float(percent) < 75:
                            droplist.append(field)
                            keeplist.remove(field)
                    else:
                        summary.append("No attributes were found for field {}".format(field.name))
                        droplist.append(field)
                        keeplist.remove(field)
                        percent = 0.0
                elif field in droplist:
                    percent = 0.0

                if field in droplist and field not in keeplist:
                    flag = "drop"
                elif field in keeplist and field not in droplist:
                    flag = "pass"
                elif field in keeplist and field not in droplist:
                    flag = "error, in both lists"

                if field.type.upper() not in ["BLOB", "GEOMETRY", "OID", "GUID"] and field.name.upper() not in ["SHAPE_LENGTH", "SHAPE_AREA", "SHAPE", "GUID"]:
                    logging(htmlfile, """<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td>
                    <td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(
                        field.name, field.aliasName, field.domain, field.editable, field.isNullable,
                        field.length, field.precision, field.required, field.scale, field.type, counts, flag, percent))

            logging(htmlfile, """</table>""")

            indexes = desc.indexes
            logging(htmlfile, """ <tr><td>
                        <button type='button' onclick='changetable("{0}_index")';>----Table {0}: Indexes</button>
                        </td></tr>
                        <tr><td>
                        <table class='maintable' id='{0}_index'>
                        <tbody>
                        <tr>
                            <th data-sort='name'><b>name of Index </b></th>
                            <th><b>is index ascending? </b></th>
                            <th><b>is index unique? </b></th>
                        </tr>""".format(table))

            for index in indexes:
                    logging(htmlfile, """<tr><td>{}</td><td>{}</td><td>{}</td></tr>""".format(index.name, index.isAscending,
                                                                                    index.isUnique))
           
        logging(htmlfile, """ </tbody>
                    </table>
            </body>
    </html>""")

    print("Complete --------------------------------------------------------------------")

except Exception as e:
    print("{} :: {}".format(arcpy.GetMessages(), e.message))





