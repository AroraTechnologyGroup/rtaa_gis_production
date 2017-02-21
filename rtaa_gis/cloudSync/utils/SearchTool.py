from arcgis.gis import GIS
import json
import os

cred = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'creds.json'), 'r').read()
j_cred = json.loads(cred)
user, pwd = [j_cred.username, j_cred.password]

class SearchTool:
    def __init__(self, type):
        self.type = type
        pass

    def search_all(self):
        gis = GIS("https://rtaa.maps.arcgis.com", user, pwd)
        search_result = gis.content.search(query="", item_type=self.type)
        return search_result

if __name__ == "__main__":
    x = SearchTool("Feature Layer")
    layers = x.search_all()
    print(layers)



