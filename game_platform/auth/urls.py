from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

urlpatterns = patterns('',
    url(r'^login', 'game_platform.auth.views.loginRequest', name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^signup$', 'game_platform.auth.views.registration', name='signup'),
    url(r'^confirm/(?P<activation_key>\w+)/', 'game_platform.auth.views.register_confirm'),
)
