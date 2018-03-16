import os
import time
import sys
import logging
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'rtaa_gis.settings'
django.setup()
from django.conf import settings

from fileApp.utils import domains
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from fileApp.models import EngineeringFileModel as FileModel
from fileApp.serializers import EngSerializer as FileSerializer

BASE_DIR = settings.BASE_DIR


class MyHandler(PatternMatchingEventHandler):
    o = domains.FileTypes()
    step1 = iter(o.file_type_choices.values())
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
                logging.info("Updated file {}".format(_data["file_path"]))
            else:
                serializer = FileSerializer()
                _data['comment'] = ""
                instance = serializer.create(_data)
                instance.save()
                logging.info("Created file {}".format(_data["file_path"]))

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

    def on_deleted(self, event):
        if not event.is_directory:
            # source_path = os.path.join(path_input, event.src_path)
            logging.info('%s :: %s' % (event.event_type, event.src_path))
            # file_path = os.path.join(path_input, event.src_path)

            try:
                x = FileModel.objects.get(file_path=event.src_path)
                x.delete()
                logging.info("Deleted {}".format(event.src_path))
            except FileModel.DoesNotExist:
                logging.warning("File removed from directory, {}, did not exist in database.".format(event.src_path))

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
                # update the data with the file_path and comments
                instance = serializer.update(file_object, _data)
                instance.save()
                logging.info("Updated file {}".format(_data['file_path']))
            else:
                serializer = FileSerializer()
                _data['comment'] = ""
                instance = serializer.create(_data)
                instance.save()
                logging.info("Create new file {}".format(_data['file_path']))


if __name__ == "__main__":
    try:
        log_path = os.path.join(BASE_DIR, "logs/watch_dog.log")
        if not os.path.exists(log_path):
            f = open(log_path, 'w')
            f.close()

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
            i = 0
            while True:
                i += 1
                time.sleep(1)
                if i % 5 == 0:
                    logging.info("{} iterations for logger".format(i))

        except KeyboardInterrupt:
            observer.stop()

        observer.join()

    except Exception as e:
        logging.error('%s' % e)

