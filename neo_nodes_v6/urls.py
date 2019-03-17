
from django.urls import path
from django.conf.urls import url
from neo_nodes_v6 import views

app_name='neo_nodes_v6'

urlpatterns = [
      url(r'nodes/',views.add_nodes,name='nodes_create'),
      url(r'ajax_form/',views.insert_form,name='insert_form'),
      url(r'edges/',views.add_edges,name='edges_create'),
     ]


