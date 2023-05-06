import os
from django.apps import AppConfig
import threading
import time

from DjangoDB.updating import keepUpdatingDatabase, hasAllCountriesBeenUpdated, getSlugList, crateTodayUpdateList


class DjangodbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DjangoDB'
    getSlugList()
    # def ready(self):
    #     my_thread1 = threading.Thread(target=UpdateInBackground, daemon=True)
    #     my_thread1.start()
def UpdateInBackground():
    my_thread = threading.Thread()
    while not hasAllCountriesBeenUpdated():
        if my_thread.is_alive():
            pass
        else:
            my_thread = threading.Thread(target=keepUpdatingDatabase)
            my_thread.start()
        time.sleep(300)
    pass