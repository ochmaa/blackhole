from django.db import models

class TelephoneOperator(models.Model):
    name  = models.CharField(max_length=200)
    prefixes = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

class Inbox(models.Model):
    phone = models.CharField(max_length=20)
    recievedate = models.DateTimeField()
    is_processed = models.BooleanField()

class Program(models.Model):
    appname = models.CharField(max_length=200)
    ip = models.CharField(max_length=20)
    keyword = models.CharField(max_length=100)
    priority = models.IntegerField()
    key = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    class Meta:
        ordering = ['priority']

class Outbox(models.Model):
    phone = models.CharField(max_length=20)
    content = models.CharField(max_length=140)
    app = models.ForeignKey(Program)
    processed = models.BooleanField()
