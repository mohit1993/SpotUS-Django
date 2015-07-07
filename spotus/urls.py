"""spotus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
import accounts.views
from django.conf import settings
from django.contrib import admin
from accounts.models import UserAccount,OrganiserAccount
from django.conf.urls.static import static
import eventhandler.views

urlpatterns = [
    url(r'^/?$',eventhandler.views.EventsView.as_view(),name = 'home'),
	#url(r'^admin/', include(admin.site.urls)),
    url(r'^user/register/?$',accounts.views.UserRegistrationView.as_view(),name = 'user_register'),
    url(r'^events/?$',eventhandler.views.EventsView.as_view(),name = 'mainview'),
    url(r'^user/login/',accounts.views.UserLoginView.as_view(),name = 'user_login'),
    
    url(r'^user/(?P<pk>[0-9]+)/?$',accounts.views.UserRedirect.as_view()),
    url(r'^user/(?P<pk>[0-9]+)/(?P<slug>[a-zA-Z0-9-]+)/?$',accounts.views.UserProfileView.as_view(),name = 'user_profile'),

    url(r'^organiser/register/?$',accounts.views.OrganiserRegistrationView.as_view(),name = "organiser_register"),
    url(r'^organiser/(?P<pk>[0-9]+)/?$',accounts.views.OrganiserRedirect.as_view()),
    url(r'^organiser/(?P<pk>[0-9]+)/(?P<slug>[a-zA-Z0-9-]+)/?$',accounts.views.OrganiserProfileView.as_view(),name = 'organiser_profile'),
    url(r'^organiser/login',accounts.views.OrganiserLoginView.as_view(),name = 'organiser_login'),

    url(r'^logout',accounts.views.LogoutView.as_view(),name = 'logout'),
    #url(r'^login/','accounts.views.LoginPage.as_view()',name = 'login'),
    #url(r'^logout/','<div class = "loginField">accounts.views.LogoutPage.as_view()',name = 'logout'),
    #url(r'^accounts/',include('allauth.urls')),

    url(r'^newevent/?$',eventhandler.views.NewEventRegister.as_view(),name = "newevent"),
    url(r'^event/(?P<pk>[0-9]+)/?$',eventhandler.views.SingleEventViewRedirect.as_view(),name = "event-redirect"),
    url(r'^event/(?P<pk>[0-9]+)/(?P<slug>[a-zA-Z0-9-]+)/?$',eventhandler.views.SingleEventView.as_view(),name = 'eventdetail'),
    ]

if settings.DEBUG:
	urlpatterns += (
		url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
		)

