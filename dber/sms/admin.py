from django.contrib import admin
from dber.sms.models import *

admin.site.register(AppUser)
admin.site.register(TelephoneOperator)
admin.site.register(Plan)
admin.site.register(Rule)
