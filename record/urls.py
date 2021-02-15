from django.conf.urls import url
from record import views

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    #url(r'^api$', views.record_list),
    #url(r'^flux', views.record_database_influx),
    url(r'^timescale/(?P<start>[\w\d-]+)&(?P<finish>[\w\d-]+)&(?P<group_time>[\w\d]+)$', views.record_database_timescale),
    #url(r'^api/record/(?P<start>[\w\d-]+)&(?P<finish>[\w\d-]+)&(?P<group_time>[\w\d]+)$', views.record_detail)
]

urlpatterns = format_suffix_patterns(urlpatterns)
