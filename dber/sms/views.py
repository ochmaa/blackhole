from django.http import *
from dber.sms.models import *
from django.shortcuts import render_to_response
from django.views.generic import create_update
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

@login_required()
def home(request):
    return render_to_response('my.html',context_instance=RequestContext(request))

def inbox(request):
    pass

def outbox(request):
    print request.GET['to']
    print request.GET['content']
    return HttpResponse()
