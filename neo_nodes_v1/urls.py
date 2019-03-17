from django.conf.urls import url,include
from neo_nodes_v1 import views

app_name="neo_nodes_v1"

urlpatterns=[
    url(r'create/',views.create,name='create'),
    url(r'read/',views.read,name='read'),
    #url(r'country/',views.add_country_func,name='country'),
#url(r'query/',views.add_query,name='query'),
]