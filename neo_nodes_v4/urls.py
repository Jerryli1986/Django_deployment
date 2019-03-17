from django.conf.urls import url,include
from neo_nodes_v4 import views

app_name="neo_nodes_v4"

urlpatterns=[
    url(r'create/',views.create,name='create'),
    url(r'create/',views.read,name='read'),
    #url(r'country/',views.add_country_func,name='country'),
#url(r'query/',views.add_query,name='query'),
]