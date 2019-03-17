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
    context={'key':'Welcome to Django-Neo4j-V2 page!'}
    return render(request, 'neo_nodes_v2/index.html', context)


def create(request):
    context={}
    result=[]
    form_label = LabelForm(request.POST or None)
    AttributeFormset=modelformset_factory(Attribute,form=AttributeForm)
    formset=AttributeFormset(request.POST or None,queryset=Attribute.objects.none())
    if request.method=="POST":
        if form_label.is_valid():
           label=form_label.save()
           label_name = label.label    # first label is instance , second label is attribute
           if formset.is_valid():
               properties={}
               for att in formset:      # att.cleaned_data  -->{'attr_name': 'AFDAS', 'attr_value': 'FAF', 'id': None}
                   data = att.save(commit=False)
                   data.label_name=label    ## hardcode
                   data.save()
                   if att.cleaned_data:
                       key = att.cleaned_data['attr_name']
                       value = att.cleaned_data['attr_value']
                       properties.update({key: value})
               graph.create(Node(label_name, **properties))

               matcher = NodeMatcher(graph)
               result = matcher.match(label_name, **properties)
           else:
                graph.create(Node(label_name))
                result=[]


    context={
        'form_label':form_label,
        'formset':formset,
        'result':result,

    }
    return render(request, 'neo_nodes_v2/create.html', context)


def add_query(request):
    form = QueryForm()
    data=[]
    if request.method == 'POST':
        form = QueryForm(request.POST)
        print(form.data)
        if form.is_valid():
            query=form['query_'].value()
            print(query)
            data =graph.run(str(query)).to_table()
            #print(data.to_subgraph())
            for d in data:
                print(d)
    else:
        form = QueryForm()

    context={'query_form':form,
             'data':data,}

    return render(request,'neo_nodes_v2/query.html',context)


def read(request):
    context = {}
    result=[]
    form_label = LabelForm(request.POST or None)
    AttributeFormset = modelformset_factory(Attribute, form=AttributeForm)
    formset = AttributeFormset(request.POST or None, queryset=Attribute.objects.none())
    if request.method == "POST":
        if form_label.is_valid():
            label = form_label.save()   #  label = form_label.save()
            label_name = label.label  # first label is instance , second label is attribute
            if formset.is_valid():
                properties = {}
                for att in formset:  # att.cleaned_data  -->{'attr_name': 'AFDAS', 'attr_value': 'FAF', 'id': None}
                    data = att.save(commit=False)
                    data.label_name = label  ## hardcodel
                    #data.save()
                    print(att.cleaned_data)
                    if att.cleaned_data :
                        key = att.cleaned_data['attr_name']
                        value = att.cleaned_data['attr_value']
                        properties.update({key: value})

                matcher = NodeMatcher(graph)
                result= matcher.match(label_name,**properties)
                # result = graph.run('Match(n:{}{}) Return n'.format(label_name,properties))
            else:
                result = graph.run('Match(n:{}) Return n'.format(label_name))
        else:
             result=[]
    context = {
        'form_label': form_label,
        'formset':formset,
        'result': result,

    }
    return render(request, 'neo_nodes_v2/read.html', context)


def update(request):
    context = {}
    result=[]
    form_label = LabelForm(request.POST or None)
    AttributeFormset = modelformset_factory(Attribute, form=AttributeForm)
    formset = AttributeFormset(request.POST or None, queryset=Attribute.objects.none())
    if request.method == "POST":
        if form_label.is_valid():
            label = form_label.save()
            label_name = label.label  # first label is instance , second label is attribute
            if formset.is_valid():
                properties = {}
                for att in formset:  # att.cleaned_data  -->{'attr_name': 'AFDAS', 'attr_value': 'FAF', 'id': None}
                    data = att.save(commit=False)
                    data.label_name = label  ## hardcode
                    data.save()
                    print(att.cleaned_data)
                    if att.cleaned_data :
                        key = att.cleaned_data['attr_name']
                        value = att.cleaned_data['attr_value']
                        properties.update({key: value})
                 #graph.run('Match(n:{}) Return n'.format(label_name))
                # matcher = NodeMatcher(graph)
                # result = matcher.match(label_name, **properties)
                # Node(label_name, **properties)
                # MERGE(n: Node {} SET n=   properties
                # {name: 'John'})
                # SET
                # n = {name: 'John', age: 34, coat: 'Yellow', hair: 'Brown'}
                # RETURN
                # n
                #graph.merge(Node(label_name, **properties))
                matcher = NodeMatcher(graph)
                result= matcher.match(label_name,**properties)
                # result = graph.run('Match(n:{}{}) Return n'.format(label_name,properties))
            else:
                result = graph.run('Match(n:{}) Return n'.format(label_name))
        else:
             result=[]
    context = {
        'form_label': form_label,
        'formset':formset,
        'result': result,

    }
    return render(request, 'neo_nodes_v2/update.html', context)








def delete(request):
    context = {}
    result=[]
    form_label = LabelForm(request.POST or None)
    AttributeFormset = modelformset_factory(Attribute, form=AttributeForm)
    formset = AttributeFormset(request.POST or None, queryset=Attribute.objects.none())
    if request.method == "POST":
        if form_label.is_valid():
            label = form_label.save()
            label_name = label.label  # first label is instance , second label is attribute
            if formset.is_valid():
                properties = {}
                for att in formset:  # att.cleaned_data  -->{'attr_name': 'AFDAS', 'attr_value': 'FAF', 'id': None}
                    data = att.save(commit=False)
                    data.label_name = label  ## hardcode
                    data.save()
                    print(att.cleaned_data)
                    if att.cleaned_data :
                        key = att.cleaned_data['attr_name']
                        value = att.cleaned_data['attr_value']
                        properties.update({key: value})

                matcher = NodeMatcher(graph)
                result= matcher.match(label_name,**properties)
                # result = graph.run('Match(n:{}{}) Return n'.format(label_name,properties))
            else:
                result = graph.run('Match(n:{}) Return n'.format(label_name))
        else:
             result=[]
    context = {
        'form_label': form_label,
        'formset':formset,
        'result': result,

    }
    return render(request, 'neo_nodes_v2/delete.html', context)
