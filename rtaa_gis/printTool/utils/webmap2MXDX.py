import os
import shutil
import sys
import subprocess
from subprocess import PIPE
import json
import logging
import argparse
import traceback
import datetime
import platform
if platform.system() == 'Windows':
    import win32security
    import win32api
    import win32con
    pass


logfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs/print_log.log")
if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")):
    os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"))

f = open(logfile, 'w')
f.close()

def logger(text):
    log_file = open(logfile, 'a')
    log_file.write("{}\n".format(text))
    log_file.close()


def format_name(text):
    nm = text.replace("_", " ")
    d = nm.replace(" ", "").lower()
    return d

try:
    import arcpy
    from arcpy import mp
    from arcpy import env
    from arcpy import Extent
    from arcpy import ExecuteError
    env.overwriteOutput = True
except Exception as e:
    logger(e)

try:
    import repairMapLayers
    from repairMapLayers import LayerRepairTool
except ImportError:
    from .repairMapLayers import LayerRepairTool

username = "gissetup"

environ = "production"

media_dir = {
    "home": "C:/Users/rich/PycharmProjects/rtaa_gis/rtaa_gis/media",
    "work": "C:/GitHub/rtaa_gis/rtaa_gis/media",
    "staging": "C:/inetpub/django_staging/rtaa_gis/rtaa_gis/media",
    "production": "C:/inetpub/django_prod/rtaa_gis/rtaa_gis/media",
}
media_dir = media_dir[environ]

gdb_path = {
    "home": r"G:\GIS Data\Arora\rtaa\MasterGDB_05_25_16\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb",
    "work": r"C:\ESRI_WORK_FOLDER\rtaa\MasterGDB\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb",
    "staging": r"C:\inetpub\rtaa_gis_data\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb",
    "production": r"C:\inetpub\rtaa_gis_data\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb"
}
gdb_path = gdb_path[environ]

default_project = {
    "home": r"G:\Documents\ArcGIS\Projects\RTAA_Printing_Publishing\RTAA_Printing_Publishing.aprx",
    "work": r"C:\Users\rhughes\Documents\ArcGIS\Projects\RTAA_Printing_Publishing\RTAA_Printing_Publishing.aprx",
    "staging": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\RTAA_Printing_Publishing.aprx",
    "production": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\RTAA_Printing_Publishing.aprx"
}
default_project = default_project[environ]

layer_dir = {
    "home": r"G:\GIS Data\Arora\rtaa\layers",
    "work": r"C:\ESRI_WORK_FOLDER\rtaa\layers",
    "staging": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\FeatureLayers",
    "production": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\FeatureLayers"
}
layer_dir = layer_dir[environ]

layout_name = "11_17_landscape"
map_title = "RTAA GIS Map"

# if len(sys.argv) == 1:
#     web_map_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests/webmap.json")
#     webmap = open(web_map_file, 'r').read()
#     webmap = json.loads(webmap)

page_title = r"RTAA Airport Authority Test Print"


def set_center_scale(webmap_as_json, map_frame):
    webmap = json.loads(webmap_as_json)
    op_layers = webmap["operationalLayers"][1:]
    map_options = webmap["mapOptions"]

    # Get the extent from the web map and project the center point into State Plane
    e = map_options["extent"]
    spatial_ref = e["spatialReference"]["wkid"]
    middle_point = arcpy.Point((e["xmax"] + e["xmin"]) / 2.0, (e["ymax"] + e["ymin"]) / 2.0)
    # lower_left = arcpy.Point(e["xmin"], e["ymin"])
    # upper_right = arcpy.Point(e["xmax"], e["ymax"])
    old_sr = arcpy.SpatialReference(spatial_ref)
    middle_geo = arcpy.PointGeometry(middle_point, old_sr)
    # ll_geo = arcpy.PointGeometry(lower_left, old_sr)
    # ur_geo = arcpy.PointGeometry(upper_right, old_sr)

    new_sr = arcpy.SpatialReference(6523)
    proj_mid_json = middle_geo.projectAs(new_sr)
    proj_mid_json = proj_mid_json.JSON
    proj_mid = json.loads(proj_mid_json)

    # proj_ll_json = ll_geo.projectAs(new_sr)
    # proj_ll_json = proj_ll_json.JSON
    # proj_ll = json.loads(proj_ll_json)
    #
    # proj_ur_json = ur_geo.projectAs(new_sr)
    # proj_ur_json = proj_ur_json.JSON
    # proj_ur = json.loads(proj_ur_json)

    # new_extent = arcpy.Extent(proj_ll["x"], proj_ll["y"], proj_ur["x"], proj_ur["y"])
    cam_X = proj_mid["x"]
    cam_Y = proj_mid["y"]
    scale = map_options["scale"]

    camera = map_frame.camera
    camera.scale = scale
    camera.X = float(cam_X)
    camera.Y = float(cam_Y)

    return op_layers


class ArcProPrint:
    def __init__(self, username, media, webmap, gdbPath, defaultProject, layerDir, layout):
        self.username = username
        self.media_dir = media
        self.webmap = webmap
        self.gdb_path = gdbPath
        self.default_project = defaultProject
        self.layer_dir = layerDir
        self.layout = layout

    def stage_project(self):
        try:
            logger("stage_project")
            out_dir = os.path.join(self.media_dir, self.username)
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            out_dir = os.path.join(out_dir, 'prints')
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)

            print_dir = out_dir
            project_file = []
            for file in os.listdir(print_dir):
                name, extension = os.path.splitext(file)
                if extension == ".aprx":
                    project_file.append(os.path.join(print_dir, file))
                    logger("this is your project file :: {}".format(file))
                    break
            if len(project_file):
                return project_file[0]
            else:
                # repair any broken layers before copying project
                lrp = LayerRepairTool(self.default_project)
                # returns project saved with layers saved in map
                aprx = lrp.repair(target_gdb=self.gdb_path)

                # copy_project = shutil.copy2(default_project, out_dir)
                logger("saving copy of aprx")
                out_name = os.path.join(print_dir, "rtaa-print.aprx")
                aprx.saveACopy(out_name)
                if os.path.exists(out_name):
                    logger("successfully saved arcpo project")
                else:
                    logger("failed to save copy of master pro project")
                return out_name

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger(traceback.print_tb(exc_traceback))

    def print_page(self):
        out_dir = os.path.join(self.media_dir, self.username)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        out_dir = os.path.join(out_dir, 'prints')
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        aprx_path = self.stage_project()
        aprx = arcpy.mp.ArcGISProject(aprx_path)
        lyt = aprx.listLayouts(self.layout)[0]
        title = lyt.listElements("TEXT_ELEMENT", "TITLE")[0]
        title.text = "BETA - Viewer Map Print"
        map_frame = lyt.listElements("MAPFRAME_ELEMENT")[0]
        map = map_frame.map
        broken_layers = [x for x in map.listBrokenDataSources() if x.isFeatureLayer]
        if len(broken_layers):
            lrp = LayerRepairTool(aprx_path)
            # returns project saved with layers saved in map
            aprx = lrp.repair(target_gdb=self.gdb_path)

        op_layers = set_center_scale(self.webmap, map_frame)
        visible_layers = {}

        op_layers = [x for x in op_layers if x["id"] not in ['labels', 'map_graphics']]

        def create_drawing_json(name, input):
            # os.chdir(out_dir)
            f = open(os.path.join(out_dir, name), 'w')
            f.write(input)
            f.close()

        for x in op_layers:
            try:
                draw_order = op_layers.index(x)
                logger(x.keys())
                if "title" not in x.keys():
                    fcoll = x["id"]
                    logger(fcoll)
                    if "graphicsLayer" in fcoll:
                        if len(x["featureCollection"]["layers"]):
                            drawing = json.dumps(x)
                            c = datetime.date.today()
                            v = c.strftime("%A %d %B %Y")
                            name = "{}.json".format(v.replace(" ", "_"))

                            i = 1
                            trig = True
                            while trig:
                                if os.path.exists(os.path.join(out_dir, name)):
                                    name = name.split(".")[0]

                                    name = "{}_{}.json".format(name, i)
                                    if not os.path.exists(os.path.join(out_dir, name)):
                                        create_drawing_json(name, drawing)
                                        trig = False
                                    else:
                                        i += 1
                                        name = name.split(".")[0]
                                        name = "_".join(name.split("_")[:-1])
                                        name = "{}.json".format(name)
                                else:
                                    create_drawing_json(name, drawing)

                else:
                    service_name = x["title"].replace("_", " ")
                    title = format_name(x["title"])
                    opacity = x["opacity"]
                    url = x["url"]
                    if title not in visible_layers.keys():
                        visible_layers[title] = {}

                    visible_layers[title]["opacity"] = opacity
                    visible_layers[title]["draw_order"] = draw_order
                    visible_layers[title]["service_name"] = service_name
                    visible_layers[title]["url"] = url
            except Exception as e:
                logger("Exception 219 :: {}".format(e))

        source_layers = map.listLayers()
        source_layers = [x for x in source_layers if x.isFeatureLayer]
        existing_layers = {}
        for x in source_layers:

            formatted_name = format_name(x.name)
            logger("formatted name = {}".format(formatted_name))
            existing_layers[formatted_name] = x
            """
            This is the link between the layers in the mxdx and the layers in the web map.
            Both of these values are passed through the format_name() function
            #TODO-Look into making the editing of layer names disabled.
            """
            if formatted_name not in visible_layers.keys():
                logger("this feature layer was not found in web map operational layers :: {}".format(formatted_name))
                try:
                    map.removeLayer(x)
                except Exception as e:
                    logger("Unable to remove layer from map :: {}".format(e))

        # The only layers being added should be raster layers, CAD?
        # add_layers = [x for x in visible_layers.keys() if x not in existing_layers.keys()]
        # for root, dirs, files in os.walk(self.layer_dir):
        #     for file in files:
        #         if file.endswith(".lyrx"):
        #             filename = format_name(file.replace(".lyrx", ""))
        #             if filename in add_layers:
        #                 layer_path = os.path.join(root, file)
        #                 lf = mp.LayerFile(layer_path)
        #                 lf.opacity = visible_layers[filename]["opacity"]
        #                 draw_order = visible_layers[filename]["draw_order"]
        #                 lyrs = map.listLayers()
        #                 map.addLayer(lf, "BOTTOM")
        #                 logger("{} layer added at bottom of TOC".format(lf))

        # Reorder Layers and set opacity
        source_layers = self.reorder_layers(map, visible_layers)
        try:
            # aprx.save()

            i = True
            num = 1
            # os.chdir(out_dir)
            output_name = "map_print"
            # ignore the extension when naming files
            files = [os.path.splitext(x)[0] for x in os.listdir(out_dir)]
            while i:
                if output_name in files:
                    output_name = "map_print{}".format(num)
                    num += 1
                else:
                    i = False

            logger("about to export file {}".format(os.path.join(out_dir, output_name)))
            # lyt = aprx.listLayouts(self.layout)[0]
            logger("using the layout named {}".format(lyt.name))
            # logger("{}".format([x.name for x in lyt.listElements()]))
            logger("{}".format(lyt.name))
            logger("{}, {}, {}".format(lyt.pageHeight, lyt.pageUnits, lyt.pageWidth))
            logger("These are layers of the map shown in the layout :: {}".format(
                [x.name for x in map.listLayers() if x.isFeatureLayer]))
            logger("These layers have broken data sources :: {}".format(
                [x.name for x in map.listBrokenDataSources()]))
            try:

                # aprx = arcpy.mp.ArcGISProject(aprx_path)
                # lyt = aprx.listLayouts(self.layout)[0]
                # logger(lyt)
                try:
                    x = lyt.exportToPDF("test")
                except Exception as e:
                    logger(e)

                if x:
                    logger("output file created named {}".format(x))
                else:
                    logger("failed to export PDF :: {}".format(x))
                return x
            except Exception as e:
                logger(e)

        except Exception as e:
            logger(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            return "Exception 292 :: {}".format(sys.exc_traceback(exc_traceback))

    @staticmethod
    def reorder_layers(mxdx, op_layers):
        all_layers = mxdx.listLayers()
        source_layers = [x for x in all_layers if x.isFeatureLayer]
        web_layers = [x for x in all_layers if x.isWebLayer]

        for x in web_layers:
            try:
                x.transparency = 100
            except Exception as e:
                logger("unable to set transparency on {}".format(e))

        for x in source_layers:
            try:
                formatted_name = format_name(x.name)

                try:
                    opacity = op_layers[formatted_name]["opacity"]
                    x.transparency = opacity * 100
                except KeyError as e:
                    pass

                draw_order = op_layers[formatted_name]["draw_order"]
                mxdx.moveLayer(all_layers[draw_order], x, "BEFORE")

            except Exception as e:
                logger("Exception 317 :: {}".format(e))

        source_layers = [x for x in all_layers if x.isFeatureLayer]
        logger("Final print layers :: {}".format([x.name for x in source_layers]))
        return source_layers


class Impersonate:
    def __init__(self, login, password):
        self.domain = 'GISAPPS'
        self.login = login
        self.password = password

    def logon(self):
        win32security.RevertToSelf()
        self.handel = win32security.LogonUser(self.login, self.domain, self.password,
                                              win32con.LOGON32_LOGON_INTERACTIVE, win32con.LOGON32_PROVIDER_DEFAULT)
        win32security.ImpersonateLoggedOnUser(self.handel)

    def logoff(self):
        win32security.RevertToSelf()
        self.handel.Close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-username', help='the username attached to the request')
    parser.add_argument('-media', help='the file path to the django media folder')
    parser.add_argument('-gdbPath', help="use the catalog Path to the master GDB")
    parser.add_argument('-defaultProject', help="use the path to the parent arcpro project")
    parser.add_argument('-layerDir', help="the parent directory storing each datasets layer files")
    parser.add_argument('-layout', help="choose the layout to print")

    args = parser.parse_args()
    logger(args)
    if args.username is not None:
        username = args.username
        if username == "Anonymous":
            username = "gissetup"
    if args.media is not None:
        media_dir = args.media
        home = os.path.join(media_dir, username)
        web_map_file = os.path.join(home, 'prints/webmap.json')
        if os.path.exists(web_map_file):
            webmap = open(web_map_file, 'r').read()
    if args.gdbPath is not None:
        gdb_path = args.gdbPath
    if args.defaultProject is not None:
        default_project = args.defaultProject
    if args.layerDir is not None:
        layer_dir = args.layerDir
    if args.layout is not None:
        layout_name = args.layout

    try:
        a = Impersonate(username, "AroraGIS123:)")
        a.logon()
        logger(a)
        p = ArcProPrint(username, media_dir, webmap, gdb_path, default_project, layer_dir, layout_name)
        x = p.print_page()
        print(x)
        a.logoff()
    except Exception as e:
        logger(e)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        sys.stderr.write(traceback.print_tb(exc_traceback))
