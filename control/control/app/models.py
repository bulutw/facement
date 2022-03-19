from django.db import models

class Client(models.Model):
    client_id = models.TextField()
    is_busy = models.BooleanField()

    def __str__(self):
        return self.client_id

class Card(models.Model):
    cc_num = models.TextField()
    client = models.TextField()

class Process(models.Model):
    process_id = models.TextField(unique = True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    confirmed = models.BooleanField(null = True)

class MobileUser(models.Model):
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
    client_id = models.TextField(blank = True)