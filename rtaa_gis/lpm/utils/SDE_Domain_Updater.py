import arcpy
from arcpy import da
import os

# the FGDB downloaded from AGOL
# agol_gdb = arcpy.GetParameterAsText(0)
agol_gdb = r"D:\EsriGDB\FGDBs\Space_2_12_18\1ad746f50d6e4e568f1e60d573d3c73d.gdb"

# the SDE GDB to update
# sde_gdb = arcpy.GetParameterAsText(1)
sde_gdb = r"C:\Users\arorateam\AppData\Roaming\ESRI\Desktop10.5\ArcCatalog\OSAuth@RTAA_MasterGDB.sde"
# domain prop = [codedValues, description, domainType, name, type]

agol_obj = {}
arcpy.env.workspace = agol_gdb
try:
    for x in arcpy.da.ListDomains(agol_gdb):
        agol_obj[x.name.strip()] = x
except Exception as e:
    print(e)

sde_obj = {}
arcpy.env.workspace = sde_gdb
try:
    for x in arcpy.da.ListDomains(sde_gdb):
        sde_obj[x.name.strip()] = x
except Exception as e:
    print(e)

# Update the SDE GDB domains with new values and remove values not included in update ie. active agreements
for x in sorted(agol_obj.keys()):
    src_dom = agol_obj[x]
    target_dom = sde_obj[x]
    domain = target_dom.name

    src_values = src_dom.codedValues
    target_values = target_dom.codedValues
    if src_values != target_values:
        for val in sorted(src_values.keys()):
            if val:
                if val not in target_values.keys():
                    value = src_values[val]

                    arcpy.AddCodedValueToDomain_management(sde_gdb, domain, val, value)

        codes = []
        for val in target_values.keys():
            if val not in src_values.keys():
                codes.append(val)
        if codes:
            if list(set(codes)) == [""]:
                string = " "
            else:
                string = ";".join(codes)

            try:
                # arcpy.DeleteCodedValueFromDomain_management(sde_gdb, domain, string)
                pass
            except Exception as e:
                print(e)

