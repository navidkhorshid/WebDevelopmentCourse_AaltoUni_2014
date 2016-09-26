__author__ = 'Navid'
from django.conf.urls import patterns, url
from game_platform.game.views import *

urlpatterns = patterns("",
    # url(r'^all$', GameListView.as_view(), name='game_list'),
    url(r'^all$', all_games, name='game_list'),
    url(r"^(?P<pk>\d+)/$", GameDetailView.as_view(), name='game_detail'),
    url(r"^cat/(\d+)$", show_category),
    url(r"^popular$", popular_games, name='popular_games'),
    url(r"^$", show_category, name='home'),
    #Author: Ligia
    url(r"^play/(\d+)$", showScore),
    url(r'^score/$', submitScore, name="updatescore"),
    url(r'^save/$', saveGame, name="savegame"),
    url(r'^load/$', loadGame, name="loadgame"),
)