from django.conf.urls import url
from policy import views

urlpatterns = [
    url(r'^$', views.policy, name='policy'),
]