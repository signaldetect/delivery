from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^customer/', include('customer.urls', namespace='customer')),
    url(r'', include('info.urls', namespace='info')),
)
