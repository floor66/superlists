from django.conf.urls import patterns, include, url
from django.contrib import admin

from lists.views import NewListView, ViewAndAddToListView

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^(?P<pk>\d+)/$', ViewAndAddToListView.as_view(), name='view_list'),
	url(r'^new$', NewListView.as_view(), name='new_list'),

    # url(r'^admin/', include(admin.site.urls)),
)
