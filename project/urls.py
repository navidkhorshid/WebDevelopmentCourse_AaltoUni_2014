from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', include('game_platform.game.urls')),
    url(r'^game/', include('game_platform.game.urls')),
    url(r'^pay/', include('game_platform.payment.urls')),
    url(r'^auth/', include('game_platform.auth.urls')),
    url(r'^dev/', include('game_platform.developer.urls')),
)
