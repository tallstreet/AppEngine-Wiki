from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed
from wiki.feeds import LatestEdits
import views # relative import

feeds = {
    'latest': LatestEdits
}

urlpatterns = patterns('',
    (r'^$', views.view_page, {'slug': 'index'}),
    (r'^r/$', views.redirecter),
    (r'^latest-changes/$', views.latest_changes),
    (r'^(\w{1,30})/$', views.view_page),
    (r'^(\w{1,30})/edit/$', views.edit_page),
    (r'^(\w{1,30})/history/$', views.history),
    (r'^(\w{1,30})/history/(\d{1,6})/$', views.view_version),
    (r'^(\w{1,30})/history/(\d{1,6})/diff/$', views.previous_version_diff),
    (r'^feeds/(?P<url>.*)/$', feed, {'feed_dict': feeds}),
)
