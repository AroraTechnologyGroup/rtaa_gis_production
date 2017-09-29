import arcpy
from arcpy import mapping
import json
import os
import sys
import argparse

#Test values
# mapfile = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)), "fixtures/webmap.json")
# template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates/RTAA.mxd")
# file = open(mapfile, 'r')
# webmap = file.read()


class MXDConvert:
    def __init__(self, media_dir, username, layout, format):
        self.media_dir = media_dir
        self.username = username
        self.layout = layout
        self.format = format
        self.webmap = os.path.join(os.path.join(media_dir, username), "prints/webmap.json")
        self.template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates/RTAA.mxd")
        pass

    def process_template(self):
        try:
            wm = open(self.webmap, 'r').read()
            result = mapping.ConvertWebMapToMapDocument(wm, self.template)
            mxd = result.mapDocument

            outfile = os.path.join(os.path.join(self.media_dir, self.username), "prints/GISViewer.pdf")
            if os.path.exists(outfile):
                os.remove(outfile)
            mapping.ExportToPDF(mxd, outfile)
            sys.stdout.write(outfile)
            return
        except Exception as e:
            sys.stdout.write(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-media_dir', help='this media root for the django project')
    parser.add_argument('-username', help='the username retrieved from the request object')
    parser.add_argument('-layout', help='this will contain the layout chosen')
    parser.add_argument('-format', help='this is the file format of the print')
    args = parser.parse_args()

    if args.media_dir is not None:
        media_dir = args.media_dir
    if args.username is not None:
        username = args.username
    if args.layout is not None:
        layout = args.layout
    if args.format is not None:
        format = args.format

    conv = MXDConvert(media_dir, username, layout, format)
    print(conv.process_template())
