from django.conf.urls import patterns, include, url
from django.contrib import admin

from lists.views import NewListView, view_list

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^(\d+)/$', view_list, name='view_list'),
	url(r'^new$', NewListView.as_view(), name='new_list'),

    # url(r'^admin/', include(admin.site.urls)),
)
