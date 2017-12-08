import sys
import os
import json
import arcpy
from arcpy import env
import traceback

util_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(util_dir)

from buildGDBStore import DescribeGDB, DescribeFDataset, DescribeFClass, DescribeField

test_gdb = r"C:\ESRI_WORK_FOLDER\rtaa\MasterGDB\MasterGDB_07_27_17.gdb"
test_dataset = r"Life_Safety"
test_fc = r"ConfinedSpace_ARFF"
test_field = r"Latitude"

env.workspace = test_gdb

descGDB = DescribeGDB(test_gdb)
output = descGDB.describe()
# test that the output is JSON serializable
string_gdb = json.dumps(output)
renew_gdb = json.loads(string_gdb.decode('utf8').replace("'", '"'))
if output == renew_gdb:
    print("GDB_obj restored")
else:
    print("{} :: {}".format(output, renew_gdb))


# this is a dynamic json object with umknown keys
domain_obj = descGDB.domains()
# dump the object, then load it back and compare
string_domain = json.dumps(domain_obj)
renew_domain = json.loads(string_domain.decode('utf8').replace("'", '"'))
if domain_obj == renew_domain:
    print("{} domains restored".format(output["base_name"]))
else:
    print("{} :: {}".format(domain_obj, renew_domain))

# datasets = arcpy.ListDatasets()
datasets = [test_dataset]
for dataset in datasets:
    env.workspace = os.path.join(test_gdb, dataset)
    descDataset = DescribeFDataset(test_gdb, dataset)
    dataset_obj = descDataset.describe()
    string_dataset = json.dumps(dataset_obj)
    try:
        renew_dataset = json.loads(string_dataset.decode('utf8').replace("'", '"'))
    except ValueError as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stderr)
        sys.stdout.write(e)

    if dataset_obj == renew_dataset:
        print("{} restored".format(dataset))
    else:
        print("{} :: {}".format(dataset_obj, renew_dataset))

    fclist = arcpy.ListFeatureClasses()
    # fclist = [test_fc]
    for fc in fclist:
        descFClass = DescribeFClass(test_gdb, dataset, fc)
        fc_obj = descFClass.describe()
        string_fc = json.dumps(fc_obj)
        try:
            renew_fc = json.loads(string_fc.decode('utf8').replace("'", '"'))
        except ValueError as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stderr)
            sys.stdout.write(e)

        if fc_obj == renew_fc:
            print("{} restored".format(fc))
        else:
            print("{} :: {}".format(fc_obj, renew_fc))

        field_summary = descFClass.summarize_fields()
        string_summary = json.dumps(field_summary)
        try:
            renew_summary = json.loads(string_summary.decode('utf8').replace("'", '"'))
        except ValueError as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2, file=sys.stderr)
            sys.stdout.write(e)

        fields = [f.name for f in arcpy.ListFields(fc)]
        # fields = [test_field]
        for field in fields:
            percent = field_summary[field]["percent"]
            descField = DescribeField(test_gdb, dataset, fc, field, percent)
            field_obj = descField.describe()
            string_field = json.dumps(field_obj)
            try:
                renew_field = json.loads(string_field.decode('utf8').replace("'", '"'))
                if field_obj == renew_field:
                    print("field_obj restored")
                else:
                    print("{} :: {}".format(field_obj, renew_field))

            except ValueError as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                                          limit=2, file=sys.stderr)
                sys.stdout.write(string_field)


