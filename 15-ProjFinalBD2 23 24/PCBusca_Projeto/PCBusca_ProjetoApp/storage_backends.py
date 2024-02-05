from django.core.files.storage import FileSystemStorage
from django.conf import settings as django_settings
import os

class StaticStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = django_settings.STATIC_ROOT
        super(StaticStorage, self).__init__(*args, **kwargs)
