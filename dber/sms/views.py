from django.http import *
from dber.sms.models import *
from django.shortcuts import render_to_response
from django.views.generic import create_update

def home(request):
    return create_update.create_object(
        request,
        model = Program,
        template_name = 'index.html',
        extra_context = {
            'prlist': Program.objects.all()
        }
    )
    return render_to_response('index.html')

def inbox(request):
    pass

def outbox(request):
    pass
