from msilib.schema import Error
import sqlite3
from tkinter import E

from django.db import IntegrityError
from .models import Client
from .models import Process

import string
import random

def generate_client_id():
    while True:
        unique = True
        client_id = ""
        ps = random.randint(1,2)
        if ps == 1:
            for i in range(4):
                client_id = client_id + random.choice(string.ascii_letters)
            client_id = client_id + str(random.randint(1111,9999))
            for i in range(2):
                client_id = client_id + random.choice(string.ascii_letters)
            client_id = client_id + str(random.randint(111111,999999))
            for i in range(2):
                client_id = client_id + random.choice(string.ascii_letters)
        elif ps == 2:
            client_id = client_id + str(random.randint(1111,9999))
            for i in range(4):
                client_id = client_id + random.choice(string.ascii_letters)
            client_id = client_id + str(random.randint(1111111,9999999))
            for i in range(2):
                client_id = client_id + random.choice(string.ascii_letters)

        for get in Client.objects.all():
            if client_id == get.client_id:
                unique = False
                break

        if unique == True:
            break
            
    return client_id

def generate_process(client):
    while True:
        r = str(random.randint(111111111111111111, 999999999999999999))
        if Process.objects.filter(process_id = r).exists():
            continue
        else:
            process = Process.objects.create( process_id = r, client = client )
            break
    return process
