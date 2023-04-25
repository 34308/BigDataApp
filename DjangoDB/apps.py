import os

from django.apps import AppConfig
import threading
import time

from DjangoDB.updating import keepUpdatingDatabase


class DjangodbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DjangoDB'

    my_thread = threading.Thread(target=keepUpdatingDatabase)

    while True:
        if my_thread.is_alive():
            pass
        else:
            my_thread = threading.Thread(target=keepUpdatingDatabase)
            my_thread.start()
        time.sleep(300)




