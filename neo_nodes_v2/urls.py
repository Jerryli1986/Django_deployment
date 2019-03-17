from django.conf.urls import url,include
from neo_nodes_v2 import views

app_name="neo_nodes_v2"

urlpatterns=[
    url(r'create/',views.create,name='create'),
    url(r'read/',views.read,name='read'),
    url(r'update/', views.update, name='update'),
    url(r'delete/', views.delete, name='delete'),
    url(r'query/',views.add_query,name='query'),
    #url(r'country/',views.add_country_func,name='country'),
#url(r'query/',views.add_query,name='query'),
]