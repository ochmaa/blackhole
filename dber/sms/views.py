 # -*- coding: utf-8 -*-
from django.http import *
from dber.sms.models import *
from django.shortcuts import render_to_response
from django.views.generic import create_update
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
import re
import datetime

@login_required()
def home(request):
    return render_to_response('home.html',{
        'plan_list': Plan.objects.all()
    },context_instance=RequestContext(request))

@login_required()
def plan(request):
    return render_to_response('plan.html',{
        'plan_list': Plan.objects.all()
    },context_instance=RequestContext(request))
    
@login_required()
def statistics(request):
    chart_list = []
    chart_list.append(example_chart())
    chart_list.append(weekly_sent_chart(request.user.get_profile()))
    chart_list.append(weekly_recieve_chart(request.user.get_profile()))
    return render_to_response('sms/statistics.html', {
        'chart_list': chart_list,
        }, context_instance=RequestContext(request))

@login_required()
def reports(request):
    pass

@login_required()
def notifications(request):
    user = request.user
    a=AppUser.objects.get(user=user)
    inboxes = a.userinbox_set.all()
    outboxes = a.useroutbox_set.all()
    if request.method=='POST':
        strids = str(request.POST)
        numbers = re.findall('[0-9]{1,}',strids)
        for message_id in numbers:
            msgobj = Message.objects.get(pk=message_id)
            msgobj.unread=False
            msgobj.save()
    return render_to_response('notifications.html',{
        'outboxes': outboxes,
        'inboxes': inboxes,
    },context_instance=RequestContext(request))
        
@login_required()
def add_rule(request):
    rule = request.POST['rule']
    url = request.POST['redirecturl']
    apuser = request.user.get_profile()
    Rule.objects.create(keyword=rule,redirect_url=url,user=apuser)
    return HttpResponseRedirect(reverse('home-page'))

@login_required()
def delete_rule(request,ruleid):
    Rule.objects.get(pk=ruleid).delete()
    return HttpResponse("ok")

@login_required()
def send_sms(request):
    phones = request.POST['phone']
    content = request.POST['content']
    apuser = request.user.get_profile()
    for phone in phones.split(','):
        apuser.send_message_increment(phone,content)
    return HttpResponseRedirect(reverse('home-page'))
    

def inbox(request):
    pass

def outbox(request):
    return HttpResponse()


def weekly_sent_chart(user):
    results = []
    days =[ x for x in range(1,8)]
    weekdic = ['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    now = datetime.datetime.now()  
    checkdate = now - datetime.timedelta(days=now.weekday())
    count = 0
    for day in days:
        count = user.useroutbox_set.filter(message__ognoo__year=now.year,message__ognoo__month=now.month,message__ognoo__day=checkdate.day).count()
        checkdate = checkdate + datetime.timedelta(days=1)
        results.append({'date':weekdic[day-1],'values':[count]})
        count = 0
    chart = {
            'id': 'week_sent_chart',
            'title': 'Энэ 7 хоногийн илгээсэн мессежны график үзүүлэлт',
            'data': {
                'columns': [{'name':'Мессежний тоо'}],
                'rows': results,
            },
            'vAxis': {'title': 'Count'},
            'curveType': 'none'
        }
    return chart

def weekly_recieve_chart(user):
    results = []
    days =[ x for x in range(1,8)]
    weekdic = ['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    now = datetime.datetime.now()  
    checkdate = now - datetime.timedelta(days=now.weekday())
    count = 0
    for day in days:
        count = user.userinbox_set.filter(message__ognoo__year=now.year,message__ognoo__month=now.month,message__ognoo__day=checkdate.day).count()
        checkdate = checkdate + datetime.timedelta(days=1)
        results.append({'date':weekdic[day-1],'values':[count]})
        count = 0
    chart = {
            'id': 'week_recieve_chart',
            'title': 'Энэ 7 хоногийн илгээсэн мессежны график үзүүлэлт',
            'data': {
                'columns': [{'name':'Мессежний тоо'}],
                'rows': results,
            },
            'vAxis': {'title': 'Count'},
            'curveType': 'none'
        }
    return chart

def example_chart():
    results = []
    for x in range(1,8):
        results.append({'date':x,'values':[x*2]})
    chart = {
            'id': 'example',
            'title': 'Example',
            'data': {
                'columns': [{'name':'Total'}],
                'rows': results,
            },
            'vAxis': {'title': 'Count'},
            'curveType': 'none'
        }
    return chart
