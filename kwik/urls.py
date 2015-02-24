from django.conf.urls import patterns, include, url
from views import current_time, tester

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    (r'^',include('people.urls')),
    # (r'^posts/',include('kwiksurfs.urls')),
    (r'^', include('kwiksurfs.urls')),   #, namespace="kwiksurfs")),

    url(r'^$', current_time),
    url(r'^say_hello/$',tester),
    # url(r'^kwik/', include('kwik.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
