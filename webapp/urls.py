from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    # let our app handle all the url routings
    url("", include('tmate.urls')),

)
