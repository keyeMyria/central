from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from dames import views

router = DefaultRouter()
router.register(r'partie', views.Lobby, 'partie')

urlpatterns = [
    url(r'^sync/$', views.PartieViewset.as_view()),
    url(r'test-ws/$', views.test_ws),
    url(r'lobby/$', views.liste),
    url(r'join/(?P<pk>[0-9]+$)', views.rejoindre),
    url(r'delete/$', views.delete),
    url(r'a-qui-le-tour/$', views.qui_joue),
    url(r'a-toi-le-tour/$', views.a_toi),
    url(r'^id/$', views.id),
]+router.urls
