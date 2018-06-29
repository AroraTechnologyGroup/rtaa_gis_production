import arcpy
from arcpy import env
import json
import os
from collections import Counter
import argparse
import sys
import traceback
import datetime


class DescribeGDB:
    """Gathers details about a geodatabase"""
    def __init__(self, workspace):
        self.workspace = workspace
        self.desc = arcpy.Describe(workspace)
        pass

    def describe(self):
        if env.workspace != self.workspace:
            env.workspace = self.workspace
        _desc = self.desc
        context = dict()
        context["base_name"] = _desc.baseName
        context["catalog_path"] = _desc.catalogPath
        context["workspace_type"] = _desc.workspaceType
        context["workspace_factory_prog_ID"] = _desc.workspaceFactoryProgID
        context["release"] = _desc.release
        context["current_release"] = _desc.currentRelease
        context["connection_string"] = _desc.connectionString
        context["dataset_list"] = arcpy.ListDatasets()
        return context

    def domains(self):
        domains = arcpy.da.ListDomains(self.workspace)
        context = dict()
        for domain in domains:
            if domain.domainType == "CodedValue":
                coded_values = domain.codedValues
                context[domain.name] = dict()
                if coded_values:
                    for key in coded_values.keys():
                        context[domain.name][key] = coded_values[key]

        return context


class DescribeFDataset:
    """Gathers details about a Feature Dataset"""
    def __init__(self, workspace, dataset):
        self.gdb = arcpy.Describe(workspace).baseName
        self.workspace = os.path.join(workspace, dataset)
        self.desc = arcpy.Describe(self.workspace)

    def describe(self):
        if env.workspace != self.workspace:
            env.workspace = self.workspace
        descdata = self.desc
        props = dict()
        props["gdb_name"] = self.gdb
        props["base_name"] = descdata.baseName
        props["change_tracked"] = descdata.changeTracked
        props["dataset_type"] = descdata.datasetType
        props["is_versioned"] = descdata.isVersioned
        props["spatial_reference"] = descdata.spatialReference.factoryCode
        props["xy_resolution"] = descdata.spatialReference.XYResolution
        props["z_resolution"] = descdata.spatialReference.ZResolution
        props["pcs_name"] = descdata.spatialReference.PCSName
        props["pcs_code"] = descdata.spatialReference.PCSCode
        props["gcs_code"] = descdata.spatialReference.GCSCode
        props["gcs_name"] = descdata.spatialReference.GCSName
        # children is not a model field, these values are used to build the fc objects below
        props["children"] = arcpy.ListFeatureClasses()
        return props


class DescribeFClass:
    """Gathers information about a Feature Class"""
    def __init__(self, workspace, dataset, fclass):
        self.workspace = os.path.join(workspace, dataset)
        self.dataset = dataset
        self.fclass = fclass
        # schema is updated with key=field name, value={"percent": 0.0, "attributes": []}
        self.field_data = {"featureClass": fclass}

    def describe(self):
        if env.workspace != self.workspace:
            env.workspace = self.workspace
        fc = self.fclass

        count = 0
        with arcpy.da.SearchCursor(fc, "OID@") as cursor:
            for row in cursor:
                count += 1

        props = dict()
        descfc = arcpy.Describe(fc)
        props["catalog_path"] = descfc.catalogPath
        props["dataset"] = self.dataset
        props["base_name"] = descfc.baseName
        props["count"] = count
        props["feature_type"] = descfc.featureType
        props["hasM"] = descfc.hasM
        props["hasZ"] = descfc.hasZ
        props["has_spatial_index"] = descfc.hasSpatialIndex
        props["shape_field_name"] = descfc.shapeFieldName
        props["shape_type"] = descfc.shapeType
        # the fields is not a model field, this list is used to build field objects below
        props["field_list"] = [f.name for f in arcpy.ListFields(fc)]
        # populate the field_data dict with field names
        for f in props["field_list"]:
            self.field_data[f] = {"percent": 0.0, "attributes": []}
        return props

    def summarize_fields(self):
        if env.workspace != self.workspace:
            env.workspace = self.workspace
        system_field_names = ["SHAPE_LENGTH", "SHAPE_AREA", "SHAPE", "OBJECTID", "GLOBALID"]
        editor_field_names = ["CREATED_USER", "CREATED_DATE", "LAST_EDITED_USER", "LAST_EDITED_DATE"]
        system_field_names.extend(editor_field_names)

        # set the system fields to 100 percent completion
        in_fields = self.field_data.keys()
        # remove the featureClass key from the in_fields
        in_fields = [x for x in in_fields if x != "featureClass"]

        for x in in_fields:
            if x.upper() in system_field_names:
                self.field_data[x]["percent"] = 100.0

        search_fields = [x for x in in_fields if x.upper() not in system_field_names]

        # the array for each key will hold the attributes
        field_dict = dict()
        for fld in search_fields:
            field_dict[fld] = []

        num_rows = 0
        # open a cursor and collect attributes for percent calc, pass percent to the field object costructor
        with arcpy.da.SearchCursor(self.fclass, search_fields) as cursor:
            for row in cursor:
                dex = 0
                for item in row:
                    try:
                        name = search_fields[dex]

                        if item is None:
                            value = "None"

                        else:
                            # python 2.x has the unicode type, python 3 has the str type for unicode
                            if type(item) is unicode:
                                # remove all single and double quotes from the attribute value
                                value = item.replace("'", "")
                                value = value.replace('"', "")
                            elif type(item) is datetime.datetime:
                                value = str(item)
                            else:
                                value = item
                        # if the length of the list is greater than the number of rows throw an error
                        written_atts = field_dict[name]
                        if len(written_atts) > num_rows:
                            raise Exception("Field {} is having too many values assigned".format(name))

                        field_dict[name].append(value)
                        dex += 1

                    except Exception as e:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                                  limit=2, file=sys.stderr)
                        sys.stderr.write(e)

                # after the row is processed increase the row count
                num_rows += 1

        for f in field_dict.keys():
            att_list = field_dict[f]

            c = Counter(att_list)
            counts = c.items()
            for cnt in counts:
                self.field_data[f]["attributes"].append([cnt[0], cnt[1]])
            del c

            i = 0
            for att in att_list:
                if type(att) is unicode:
                    d = att.strip()
                else:
                    try:
                        d = float(value)
                        d = int(d)
                    except:
                        d = value

                if d not in ['', ' ', '0', 'None', '<Null>']:
                    i += 1
                del d
            if num_rows:
                percent = (float(i) / num_rows) * 100.00
            else:
                percent = 0.0

            self.field_data[f]["percent"] = percent

        return self.field_data


class DescribeField:

    def __init__(self, _workspace, _dataset, _fc, _field, _percent):
        self.workspace = os.path.join(_workspace, _dataset)
        self.fc = _fc
        self.field = _field
        self.percent = _percent

    def describe(self):
        if env.workspace != self.workspace:
            env.workspace = self.workspace
        infc = self.fc
        in_field = self.field
        field = arcpy.ListFields(infc, "{}".format(in_field))[0]
        props = dict()
        props["fc_name"] = self.fc
        # using the feature class name with the field name makes it unique
        props["name"] = "{}::{}".format(self.fc, field.name)
        props["alias_name"] = field.aliasName
        props["base_name"] = field.baseName
        props["default_value"] = field.defaultValue
        # this domain_name is used to filter for the actual objects when creating the field in views.py
        props["domain_name"] = field.domain
        props["editable"] = field.editable
        props["is_nullable"] = field.isNullable
        props["length"] = field.length
        props["precision"] = field.precision
        props["required"] = field.required
        props["scale"] = field.scale
        props["type"] = field.type
        props["percent"] = self.percent

        return props


if __name__ == "__main__":
    """
       1. If the gdb is provided and no other parameters, then the entire model will be built
       2. If the dataset is provided, then only that dataset will be analyzed
       3. If the feature class is provided, then only that feature class will be analyzed
       4. If the field is provided, the only that field will be analyzed

       * the gdb must be provided
       """

    parser = argparse.ArgumentParser()
    parser.add_argument('-gdb', help='this is the path to the geodatabase', required=True)
    parser.add_argument('-dataset', help='this is the dataset to analyze')
    parser.add_argument('-featureClass', help='this is a single feature class to analyze')
    parser.add_argument('-field', help='this is a single field to analyze')

    args = parser.parse_args()

    if args.gdb is not None:
        gdb = args.gdb
    else:
        sys.stderr.write("A Geodatabase must be provided")
        sys.exit(2)
    if args.dataset is not None:
        dataset = args.dataset
    else:
        dataset = None

    if args.featureClass is not None:
        featureClass = args.featureClass
    else:
        featureClass = None

    if args.field is not None:
        single_field = args.field
    else:
        single_field = None

    x = DescribeGDB(gdb)

    gdb_output = x.describe()
    sys.stdout.write(json.dumps(gdb_output) + "\n")

    domain_obj = x.domains()
    for domain in domain_obj.keys():
        value_dict = domain_obj[domain]
        for key in value_dict.keys():
            # the gdb is for assigning the domains to the gdb when creating the row
            domain_data = {'gdb_name': gdb_output["base_name"], 'name': domain, 'code': key, 'description': value_dict[key]}
            sys.stdout.write(json.dumps(domain_data) + "\n")

    try:
        if dataset:
            # We are only processing this one dataset
            datasets = [dataset]
        else:
            # We are going to process all of the datasets
            datasets = gdb_output["dataset_list"]

        for dataset in datasets:
            desc_dataset = DescribeFDataset(gdb, dataset)
            dset_output = desc_dataset.describe()
            sys.stdout.write(json.dumps(dset_output) + "\n")

            if featureClass:
                fclist = [featureClass]
            else:
                fclist = dset_output["children"]

            for fc in fclist:
                obj = DescribeFClass(gdb, dataset, fc)
                fc_out = obj.describe()
                sys.stdout.write(json.dumps(fc_out) + "\n")

                # if features exist summarize the fields
                if fc_out["count"]:
                    field_summary = obj.summarize_fields()
                    sys.stdout.write(json.dumps(field_summary) + "\n")

                    if single_field:
                        fields = [single_field]
                    else:
                        fields = fc_out["field_list"]

                    for fld in fields:
                        percent = field_summary[fld]["percent"]
                        f_obj = DescribeField(gdb, dataset, fc, fld, percent)
                        f_out = f_obj.describe()
                        sys.stdout.write(json.dumps(f_out) + "\n")

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stderr)
        sys.stderr.write(e)
