from django.contrib import admin

# Register your models here.

from watcher.models import Url, UrlWatchResult

admin.site.register(Url)
admin.site.register(UrlWatchResult)
