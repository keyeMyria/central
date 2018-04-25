from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/admin/(?P<id>[0-9]+)$', consumers.DamesAdmin),
    url(r'^ws/sync/(?P<id>[0-9]+)/(?P<couleur>[^/]+)$', consumers.DamesSync)
]