from arcgis.gis import GIS
import json


class SearchTool:
    def __init__(self, type):
        self.type = type
        pass

    def search_all(self):
        gis = GIS("https://rtaa.maps.arcgis.com", "data_owner", "GIS@RTAA123!")
        search_result = gis.content.search(query="", item_type=self.type)
        return search_result

if __name__ == "__main__":
    x = SearchTool("Feature Layer")
    layers = x.search_all()
    print(layers)



