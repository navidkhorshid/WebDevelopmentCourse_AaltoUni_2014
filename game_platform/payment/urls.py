from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r"^$", 'game_platform.payment.views.payment', name='payment'),
                       url(r'^success/$', 'game_platform.payment.views.success_pay', name='success_pay'),
                       url(r'^failed/$', 'game_platform.payment.views.failed_pay', name='failed_pay'),
                       )
