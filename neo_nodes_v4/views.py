from django.shortcuts import render
from django.forms import modelformset_factory
from .forms import *

import django.dispatch
from django.dispatch import receiver,Signal
from django.urls import reverse_lazy

from .models import *
from django import forms
from Test2_py2neo.settings import graph
from py2neo import Graph,Node,NodeMatcher,Relationship
# Create your views here.
def index(request):
    context={'key':'Welcome to Django-Neo4j-V1 page!'}
    return render(request, 'neo_nodes_v4/index.html', context)


def create(request):
    context={}
    form_id = NodeIdForm(request.POST or None)
    form_label = LabelForm(request.POST or None)
    AttributeFormset=modelformset_factory(Attribute,form=AttributeForm)
    formset=AttributeFormset(request.POST or None,queryset=Attribute.objects.none())
    if request.method=="POST":
        node_id = form_id.save()
        if form_label.is_valid():
           label=form_label.save()
           label_name = label.label    # first label is instance , second label is attribute
           if formset.is_valid():
               properties={}
               for att in formset:      # att.cleaned_data  -->{'attr_name': 'AFDAS', 'attr_value': 'FAF', 'id': None}
                   data = att.save(commit=False)
                   data.label_name=label    ## hardcode
                   data.node_id=node_id          ## hardcode
                   data.save()
                   key=att.cleaned_data['attr_name']
                   value = att.cleaned_data['attr_value']
                   properties.update({key:value})
                   # node_id  can not be created by Node and graph.create , it will automatically create numurical id
               graph.create(Node(label_name, **properties))
           else:
                 graph.create(Node(label_name))
    context={
        'form_id':form_id,
        'form_label':form_label,
        'formset':formset,

    }
    return render(request, 'neo_nodes_v4/create.html', context)



def read(request):
    context = {'key': 'Read page!'}
    return render(request, 'neo_nodes_v4/read.html', context)