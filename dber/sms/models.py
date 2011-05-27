from django.db import models
from django.contrib.auth.models import User

class Plan(models.Model):
    name = models.CharField(max_length=200)
    tarif = models.IntegerField()
    inbox_count = models.IntegerField(default=1000,choices = (
        ( -1, 'Unlimited'),
        ( 1000, '1000'),
        (2000, '2000'))) 
    
    def __unicode__(self):
        return self.name

class AppUser(models.Model):
    user = models.ForeignKey(User)
    plan = models.ForeignKey(Plan)
    remcash = models.IntegerField(default=15000)
    inbox_count = models.IntegerField(default=1000)

    def rules(self):
        return self.rule_set.all()
        
    def RM(self):
        return self.userinbox_set.count()
        
    def UNR(self):
        return self.userinbox_set.filter(message__unread=True).count()

    def RMP(self):
        return float(self.UNR())/float(self.RM())*100

    def SM(self):
        return self.useroutbox_set.count()

    def USM(self):
        return self.useroutbox_set.filter(message__unread=True).count()

    def SMP(self):
        return float(self.USM())/float(self.SM())*100 

    def RCP(self):    
        return float(self.remcash)/float(self.plan.tarif)*100 

    def __unicode__(self):
        return self.user.username

    def virgin(self):
        self.remcash = self.plan.tarif
        self.inbox_count = self.plan.inbox_count
        self.save()

    def send_message_increment(self,phone,content):
        msgobj = Message.objects.create(phone=phone,content=content)
        UserOutbox.objects.create(message=msgobj,user=self)
        pref = phone[:2]
        telops = TelephoneOperator.objects.filter(prefixes__contains=pref)
        for telop in TelephoneOperator.objects.all():
            if pref in telop.prefixes.split(','):
                self.remcash = self.remcash - telop.tarif
                self.save()

    def cant_recieve(self):
        return self.inbox_count==0

    def cant_reach_money(self):
        mintarif = [op.tarif for op in TelephoneOperator.objects.all()]
        return self.remcash<mintarif

    def decrement_inbox(self):
        self.inbox_count = self.inbox_count -1
        self.save()

class TelephoneOperator(models.Model):
    name  = models.CharField(max_length=200)
    prefixes = models.CharField(max_length=255)
    tarif = models.IntegerField()
    
    def __unicode__(self):
        return self.name

class Rule(models.Model):
    keyword = models.CharField(max_length=20)
    redirect_url = models.URLField()
    user = models.ForeignKey(AppUser)

    def __unicode__(self):
        return self.keyword        

class Message(models.Model):
    phone = models.CharField(max_length=20)
    content = models.CharField(max_length=150)
    ognoo = models.DateTimeField(auto_now=True)
    unread = models.BooleanField(default=True)
    
class UserInbox(models.Model):
    user = models.ForeignKey(AppUser)
    message = models.ForeignKey(Message)

    def save(self, *args, **kwargs):
        if self.user.cant_recieve():
            print 'your inbox is full'
        else:
            super(UserInbox,self).save(*args,**kwargs)            
            self.user.decrement_inbox()
            
class UserOutbox(models.Model):
    user = models.ForeignKey(AppUser)
    message = models.ForeignKey(Message)
    
