from django.conf.urls import patterns, include, url, handler404
from tmate.views import *

urlpatterns = patterns('',

    # home page
    url(r'^$', index, name='index'),

    # authendication related
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'tmate/login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^register$', register, name='register'),
    url(r'^register-entry$', register_entry, name='register_entry'),

    url(r'^profile/(?P<uid>\d+)$', profile, name='profile'),
    url(r'^search$', search, name='search'),

    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', confirm_registration, name='confirm'),

        )

handler404 = 'tmate.views.page_not_found'
