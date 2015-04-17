from django.conf.urls import patterns, include, url

from django.contrib import admin
from blogey import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blogey.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include('posts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
if not settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
