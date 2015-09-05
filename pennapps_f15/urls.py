from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

# Included App URL Patterns
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/', include('pennapps_f15.apps.users.urls', namespace='users'))
)

# Main URL Patterns
urlpatterns += patterns('',
    # url(r'^$', 'pennapps_f15.views.home'),
     url(r'^$', 'django_twilio.views.gather', {
        'action': '/process_input/'
    }),
    url(r'^process_input/$', 'pennapps_f15.views.home'),
)

# Development
from django.conf import settings
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    media = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns = media + staticfiles_urlpatterns() + urlpatterns
