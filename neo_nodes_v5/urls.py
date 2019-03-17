"""systemsmap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Nodes url.py

from django.urls import path
from django.conf.urls import url
from neo_nodes_v5 import views

app_name='neo_nodes_v5'

urlpatterns = [
      url(r'create/',views.add_nodes,name='nodes_create'),
      url(r'select/',views.select_nodes,name='select_nodes'),
      # url(r'getlist/',views.get_list,name='abc'),





]
