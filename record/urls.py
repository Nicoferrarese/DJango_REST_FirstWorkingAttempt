from django.conf.urls import url
from record import views

urlpatterns = [
    url(r'^api$', views.record_list),
    #url(r'^api/record/(?P<pk>[0-9]+)$', views.tutorial_detail) da fare simile con filtri per records
]
