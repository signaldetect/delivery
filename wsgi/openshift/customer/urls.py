from django.conf.urls import patterns, url

from customer import views

urlpatterns = patterns('',
    url(r'^$', views.Profile.as_view(), name='profile'),

    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^register/complete/$',
        views.RegisterComplete.as_view(), name='register_complete'),

    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),

    url(r'^hotline/$', views.Hotline.as_view(), name='hotline'),
    url(r'^hotline/complete/$',
        views.HotlineComplete.as_view(), name='hotline_complete'),

    url(r'^question/$', views.Question.as_view(), name='question'),
    url(r'^question/complete/$',
        views.QuestionComplete.as_view(), name='question_complete'),

    url(r'^order/$', views.Order.as_view(), name='order'),
)
