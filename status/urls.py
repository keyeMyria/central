from rest_framework import routers
from django.conf.urls import include, url
from status import views

router = routers.DefaultRouter()
router.register(r'all', views.HostsOverview)
router.register(r'detail', views.InfosViewSet, 'detail')
router.register(r'status', views.StatusViewSet, 'status')

urlpatterns = router.urls+[
    url(r'^me$', views.me),
]
