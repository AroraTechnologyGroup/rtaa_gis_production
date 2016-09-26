import os
import time
import sys
import django
import logging
import utils
from utils import buildDocStore
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


sys.path.append("{}\\_fileApp".format(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'eDocSearchAPI.settings'
django.setup()

from fileApp.models import FileModel as FileModel
from fileApp.serializers import FileSerializer as FileSerializer
from rtaa_gis.settings import BASE_DIR


class MyHandler(PatternMatchingEventHandler):

    step1 = iter(buildDocStore.FILE_TYPE_CHOICES.values())
    patterns = ["*.{}".format(list(k.keys())[0]) for k in step1]
    ignore_directories = False
    case_sensitive = False

    """
    event.event_type
        'modified' | 'created' | 'moved' | 'deleted'
    event.is_directory
        True | False
    event.src_path
        path/to/observed/file
    """

    def process(self, event):
        if not event.is_directory:
            # source_path = os.path.join(path_input, event.src_path)
            logging.info('%s :: %s' % (event.event_type, event.src_path))
            print('%s :: %s' % (event.event_type,  event.src_path))
            _data = {'file_path': event.src_path}

            if len(FileModel.objects.filter(file_path=event.src_path)):
                file_object = FileModel.objects.filter(file_path=event.src_path)[0]
                comment = file_object.comment
                _data['comment'] = comment
                serializer = FileSerializer()
                instance = serializer.update(file_object, _data)
                instance.save()
            else:
                serializer = FileSerializer()
                _data['comment'] = ""
                instance = serializer.create(_data)
                instance.save()

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

    def on_deleted(self, event):
        if not event.is_directory:
            # source_path = os.path.join(path_input, event.src_path)
            logging.info('%s :: %s' % (event.event_type, event.src_path))
            # file_path = os.path.join(path_input, event.src_path)
            x = FileModel.objects.get(file_path=event.src_path)
            x.delete()

    def on_moved(self, event):
        if not event.is_directory:
            logging.info('%s \n sourcepath - %s \n destpath - %s' % (event.event_type, event.src_path,
                                                                     event.dest_path))
            # source_path = os.path.join(path_input, event.src_path)
            # destination_path = os.path.join(path_input, event.dest_path)

            _data = {'file_path': event.dest_path}

            if len(FileModel.objects.filter(file_path=event.src_path)):
                file_object = FileModel.objects.filter(file_path=event.src_path)[0]
                comment = file_object.comment
                _data['comment'] = comment
                serializer = FileSerializer()
                instance = serializer.update(file_object, _data)
                instance.save()
            else:
                serializer = FileSerializer()
                _data['comment'] = ""
                instance = serializer.create(_data)
                instance.save()


if __name__ == "__main__":
    try:
        log_path = os.path.join(BASE_DIR, "logs/watch_dog.log")
        logging.basicConfig(
            level=logging.INFO,
            filename=log_path,
            filemode='w',
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        path_input = sys.argv[1] if len(sys.argv) > 1 else '.'
        if path_input == '.':
            path_input = os.path.dirname(os.path.abspath(__file__))

        observer = Observer()
        observer.schedule(MyHandler(), path_input, recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()

    except Exception as e:
        logging.error('%s' % e)

