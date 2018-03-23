from django.conf.urls import url
from minecraft import views

urlpatterns = [
    url(r'status', views.minecraft_status),
]