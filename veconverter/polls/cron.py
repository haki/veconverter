import os
import glob
import time
import shutil
from datetime import datetime, timedelta
from django.conf import settings


def remove_files_older_than_a_hour():
    """
    Remove all files older than 1 hour
    """
    files = glob.glob(os.path.join(settings.MEDIA_ROOT, '*'))
    for f in files:
        if os.path.isfile(f):
            if os.path.getmtime(f) < (time.time() - 3600):
                os.remove(f)
