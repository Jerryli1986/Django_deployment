from django.conf.urls import url,include
from neo_nodes import views

app_name="neo_nodes"

urlpatterns=[
    url(r'register/',views.add_register_func,name='register'),
    url(r'country/',views.add_country_func,name='country'),
url(r'query/',views.add_query,name='query'),
]