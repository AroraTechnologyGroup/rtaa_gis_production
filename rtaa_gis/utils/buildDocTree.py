import os
from . import buildDocStore
import mimetypes
from directoryObjects import FileObject

desired_files = buildDocStore.FILE_TYPE_CHOICES


class TreeBuilder:
    def __init__(self, top_dir):
        self.topDir = top_dir
        pass
    
    def build_tree(self):
        try:
            tree = {}
            top_dir = self.top_dir
            for root, dirs, files in os.walk(top_dir):
                tree[root] = []
                for _file in files:
                    if _file.split(".")[-1] in desired_files:
                        fpath = os.path.join(root, _file)
                        type = mimetypes.guess_type(fpath)
                        size = os.path.getsize(fpath)
                        file_obj = FileObject(_file, type, size, root)
                        tree[root].append(file_obj)
            return tree
            
        except Exception as e:
            print e.message
            return
