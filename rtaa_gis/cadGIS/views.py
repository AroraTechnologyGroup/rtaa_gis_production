import os
import ast
from.serializer import MySerializer
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import AllowAny
from rtaa_gis.settings import MEDIA_ROOT
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


def check_keys(a, x):
    key = x['group']

    if key.lower() == "unmatched-layer-name":
        output = {
            "group": x['group'],
            "cad_layer_name": x['cad-layer-name'],
            "shape": x['shape'],
            "status": "N/A",
            "repaired": "N/A",
            "cad_file_name": x["cad-file-name"]
        }
    else:
        output = {
            "group": x['group'],
            "cad_layer_name": x['cad-layer-name'],
            "shape": x["shape"],
            "status": x["status"],
            "repaired": x["repaired"],
            "cad_file_name": x["cad-file-name"]
        }

    if key not in a:
        a[key] = [output]
    else:

        a[key].append(output)

    return a


def process_string(f_path):
    o = open(f_path, 'r')
    text = o.read()
    spaced_string = "}, ".join(text.split("}"))
    spaced_string = spaced_string.rstrip(',')
    new_list = "[{}]".format(spaced_string)
    ast_con = ast.literal_eval(new_list)
    return ast_con


@method_decorator(csrf_exempt, name='dispatch')
class MatchNames(APIView):
    """this view will render the json file returned from ETL Conversion into the template"""

    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    permission_classes = (AllowAny, )
    template_name = r"cadGIS/match_names.html"

    def get(self, request, *args, **kwargs):
        context = {"data": []}
        f_path = os.path.join(MEDIA_ROOT, 'cadGIS/CADLayer_log.txt')
        if os.path.exists(f_path):
            my_dict = {}
            ast_con = process_string(f_path)
            for x in ast_con:
                my_dict = check_keys(my_dict, x)
            keys = my_dict.keys()
            keys.sort()
            data = context["data"]
            for k in keys:
                data.append({"key": k, "values": my_dict[k]})

        else:
            context['data'].append({"error": "the logfile was not found at the specified path"})
            return Response(context)

        if request.accepted_renderer.format == 'html':
            return Response(context, template_name=self.template_name)

        data = context["data"]
        serializer = MySerializer(instance=data['values'], many=True)
        data = serializer.data
        return Response(data)


@method_decorator(csrf_exempt, name='dispatch')
class UploadFile(APIView):
    """Upload a file into the Media folder for the app"""
    parser_classes = (FileUploadParser,)

    @staticmethod
    def handle_uploaded_file(f, filename):
        out_path = os.path.join(MEDIA_ROOT, 'cadGIS/{}'.format(filename))
        with open(out_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        self.handle_uploaded_file(file_obj, filename)
        return Response(status=204)



