from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from watcher.views import (
    url_home,
    url_list,
    UrlView,
    UrlListView,
    UrlWatcherListView
)

urlpatterns = [
    path('api/url/', UrlView.as_view()),
    path('api/url/list/', UrlListView.as_view()),
    path('api/url-watcher/<int:id>/', UrlWatcherListView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns = urlpatterns + [
    path('', url_home),
    path('list/', url_list),
]
