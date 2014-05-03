from django.conf.urls import patterns, url

from info import views

urlpatterns = patterns('',
    url(r'^$', views.Home.as_view(), name='home'),

    url(r'^news/$', views.News.as_view(), name='news'),
    url(r'^news/(?P<year>\d{4})/$', views.News.as_view(), name='news'),

    url(r'^specoffers/$', views.SpecOffers.as_view(), name='specoffers'),
    url(r'^specoffers/(?P<state>active|finished|all)/$',
        views.SpecOffers.as_view(), name='specoffers'),

    url(r'^papers/$', views.Papers.as_view(), name='papers'),

    url(r'^(?P<slug>[\w-]+)/$', views.Page.as_view(), name='page'),
)
