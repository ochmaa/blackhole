from twisted.web.resource import Resource
from twisted.web.static import File
from twisted.internet import reactor
from blackhole.admin.site import template_env
from blackhole.admin.site import MEDIA_PATH
from dber import settings
from django.core.management import setup_environ
setup_environ(settings)
from dber.sms.models import *
import urllib
import re
import datetime

url='http://localhost:13013/cgi-bin/sendsms?username=foo&password=bar&to=%s&text=%s'
class IndexPage(Resource):
    isLeaf = True

    def render_GET(self,request):
        template  = template_env.get_template('index.html')
        return template.render().encode('utf-8')

class Reciever(Resource):
    isLeaf = True

    def render_GET(self,request):
        to = request.args['to']
        content = request.args['content']
        to=to[0]
        to = to[-8:]
        firstword  = content[0].split(' ')[0]
        a = Program.objects.all()
        for program in Program.objects.all():
            if firstword in program.keyword.split(','):
                notificationurl = 'http://%s/%s'%(program.ip,program.url)
                print 'not url is ',notificationurl
                notificationurl = notificationurl%(to,content[0])
                print 'complete notification url is', notificationurl
                urllib.urlopen(notificationurl)
        Inbox.objects.create(phone=to, recievedate = datetime.datetime.now(), is_processed=True)
        if to!='88253141':
            template  = template_env.get_template('index.html')
            return template.render().encode('utf-8')

class Process(Resource):
    isLeaf = True

    def render_GET(self,request):
        self.work()
        template  = template_env.get_template('index.html')
        return template.render().encode('utf-8')
        
    def work(self):
        jobs = Outbox.objects.filter(processed=False).order_by('app')
        i = 10
        for job in jobs:
            reactor.callLater(i,self.process,job)
            i+=10

    def process(self,job):
        myurl = url%(job.phone,job.content)
        print 'url is ',myurl
        urllib.urlopen(myurl)
        job.processed=True
        job.save()

class Sender(Resource):
    isLeaf = True

    def render_GET(self,request):
        to = request.args['to']
        content = request.args['content']
        key = request.args['key']
        print key[0]
        ap = Program.objects.filter(key=key[0])
        if ap and to[0]!='88253141':
            Outbox.objects.create(phone = to[0], content = content[0],processed=False,app=ap[0]) 
            template  = template_env.get_template('index.html')
            return template.render().encode('utf-8')
        template  = template_env.get_template('notfound.html')
        return template.render().encode('utf-8')


    
root = Resource()
root.putChild('', IndexPage())
root.putChild('media', File(MEDIA_PATH))
root.putChild('server',Reciever())
root.putChild('send', Sender())
root.putChild('process',Process())
