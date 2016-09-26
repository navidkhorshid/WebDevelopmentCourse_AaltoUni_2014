__author__ = 'Navid'
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'game_platform.developer.views.dev_page', name='dev_page'),
                       url(r'^new', 'game_platform.developer.views.add_game', name='new_game'),
                       url(r"^edit/(\d+)$", 'game_platform.developer.views.edit_game', name='modify_game'),
                       url(r'^sales/$', 'game_platform.developer.views.sales_list', name='sales_list'),
                       url(r'^sales/(\d+)$', 'game_platform.developer.views.sales_game', name='sales_game'),
                       # url(r'^sales/(\d+)$', 'game_platform.developer.views.sales_chart', name='sales_chart'),
                       )
