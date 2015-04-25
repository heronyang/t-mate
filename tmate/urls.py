from django.conf.urls import patterns, include, url, handler404
from tmate.views import *

urlpatterns = patterns('',

    # home page
    url(r'^$', index, name='index'),

    # authendication related
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'tmate/login.html'}),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register$', register, name='register'),

        )

handler404 = 'tmate.views.page_not_found'
