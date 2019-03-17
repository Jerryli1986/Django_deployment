from django.shortcuts import render


import django.dispatch
from django.dispatch import receiver,Signal
from django.urls import reverse_lazy

from .models import *
from django import forms
from Test2_py2neo.settings import graph
from py2neo import Graph,Node,NodeMatcher,Relationship


# #signal
# request_register_signal=Signal()
# request_country_signal=Signal()

# create new register
class RegisterForm(forms.Form):
    name=forms.CharField(max_length=100)
    gender=forms.CharField(max_length=10)

class CountryForm(forms.Form):
    country_name=forms.CharField(max_length=100)
    population=forms.FloatField()


class QueryForm(forms.Form):
    query_=forms.CharField(max_length=256)


def index(request):
    context={'key':'Welcome to Django-Neo4j page!'}
    return render(request,'neo_nodes/index.html',context)


def add_register_func(request):
    # if request is not post, initialize an empty form
    form = RegisterForm()
    data=[]
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():

            name = form['name'].value()
            gender = form['gender'].value()
            If_exists= NodeMatcher(graph).match('Register', name=name).first()
            if not If_exists:
                register=Node('Register',name=name,gender=gender)
                graph.create(register)
                data = graph.run('Match (n:Register) Return n').to_table()
                ## SQL data
                register_sql = Register_SQL(name=name,gender=gender)
                register_sql.save()

            form = CountryForm()
    context={'register_form': form,
                 'data_register':data,}
        # request_register_signal.send(sender=Register)
    return render(request, 'neo_nodes/register_create_form.html',context)


def add_country_func(request):
    form = CountryForm()
    data=[]
    if request.method=='POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            country_name = form['country_name'].value()
            population = form['population'].value()
            If_exists= NodeMatcher(graph).match('Country', country_name=country_name).first()
            if not If_exists:
                country = Node('Country', country_name=country_name, population=population)
                graph.create(country)
                data=graph.run('Match (n:Country) Return n').to_table()
                ## SQL data
                country_sql=Country_SQL(country_name=country_name, population=population)
                country_sql.save()
        else:
            form = CountryForm()
    context = {
               'country_form': form,
                'data':data,
               }
    # request_country_signal.send(sender=Country)
    return render(request, 'neo_nodes/country_create_form.html',context)


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

    return render(request,'neo_nodes/query.html',context)

## add relationship

def add_relationship(node1,node2,**properties):
    rel=Relationship(node1,'LIVED_IN',node2,**properties)
    graph.create(rel)








# ## signal
# @receiver(request_register_signal)
# def post_request_receiver(sender, **kwargs):
#     print("Request finished!")
#
#
# @receiver(request_country_signal)
# def post_register_signal_receiver(sender, **kwargs):
#     print(kwargs)


