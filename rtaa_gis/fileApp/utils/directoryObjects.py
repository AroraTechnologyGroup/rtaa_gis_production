import os
import mimetypes


class FileObject:
    def __init__(self, name, type, size, parent):
        self.name = name
        self.type = type
        self.size = size
        self.parent = parent


class FolderObject:
    def __init__(self, path, siblings):
        try:
            self.siblings = siblings
            self.path = path
            self.name = os.path.basename(path)
            self.parent = os.path.dirname(path)
            self.children = self.get_children()
        except Exception as e:
            print(e)
        
    def get_children(self):
        try:
            files = os.listdir(self.path)
            file_objs = []
            for f in files:
                fpath = os.path.join(self.path, f) 
                type = mimetypes.guess_type(fpath)
                size = os.path.getsize(fpath)
                par = self.name
                file_obj = FileObject(f, type, size, par)
                file_objs.append(file_obj)
                
            return file_objs
        
        except Exception as e:
            print(e)
            return
