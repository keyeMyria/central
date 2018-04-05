from django.conf.urls import url
from dames import views

urlpatterns = [
        url(r'^sync/$', views.PartieViewset.as_view()),
        ]