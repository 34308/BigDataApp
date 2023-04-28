import os
from django.apps import AppConfig
import threading
import time

from DjangoDB.updating import keepUpdatingDatabase, hasAllCountriesBeenUpdated


class DjangodbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DjangoDB'
    def ready(self):
         my_thread1 = threading.Thread(target=my_function,daemon=True)
         my_thread1.start()
def my_function():
    my_thread = threading.Thread()
    beenUpdate = hasAllCountriesBeenUpdated()
    while not beenUpdate:
        if my_thread.is_alive():
            pass
        else:
            beenUpdate = hasAllCountriesBeenUpdated()
            my_thread = threading.Thread(target=keepUpdatingDatabase)
            my_thread.start()
        time.sleep(300)
    pass