from django.conf.urls.defaults import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'dber.sms.views.home', name='home'),
    url(r'^inbox$','dber.sms.views.inbox', name='inbox'),
    url(r'^outbox$','dber.sms.views.outbox', name='outbox'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login-page', kwargs = { 'template_name' : 'login.html', }),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout-page'),
    # url(r'^dber/', include('dber.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
