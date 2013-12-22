from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'lists.views.home_page', name='home'),
	url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
	url(r'^(\d+)/new_item/$', 'lists.views.new_item', name='new_item'),
	url(r'^new/$', 'lists.views.new_list', name='new_list'),

    # url(r'^admin/', include(admin.site.urls)),
)
