import pandas as pd
import re
import json
from django.http import HttpResponse
import ast
from django.shortcuts import render
from .forms import *
from .models import System,RecordSet,Region
from py2neo import Database,Graph, Node, Relationship
graph=Graph("bolt://127.0.0.1:7687",auth=("neo4j","neo4j2"))

def index(request):
    template='neo_nodes_v6/base.html'
    return render(request, template )

def add_nodes(request):
    properties = {}
    label_form=None
    form=None
    label_form = LabelForm(request.GET or None)     # because on create_nods.html has {%bootstrap label_form%} so no matter post or get, we have to render label_form
    print(request.POST)
    if request.method=='POST':
        label=request.POST.get('create_button')     # a trick to save label data to button.value
        if label=='RecordSet' :
            form= RecordSetForm(request.POST or None)
        elif label=='Region' :

            form = RegionForm(request.POST or None)
            print(form)
        elif label=='System' :
            form = SystemForm(request.POST or None)

        if form.is_valid() and form.is_bound:
            form.save()
            properties = form.cleaned_data
            print(properties)
            # graph.create(Node(label, **properties))
    context={
             'label_form': label_form,
             'form':form,
             }
    template = 'neo_nodes_v6/nodes_create.html'
    return render(request, template,context)

def insert_form(request):
    form = {}
    label={}
    if request.method=='GET':
        label = request.GET.get('label')
        if label == 'RecordSet':
            form = RecordSetForm()
        elif label == 'Region':
            form = RegionForm()
        elif label == 'System':
            form = SystemForm()
    context = {'form': form,
               'label':label}
    # return HttpResponse(form.as_p())
    return render(request, 'neo_nodes_v6/insert_form_nodes.html', context)


def add_edges(request):
    template='neo_nodes_v6/edges_create.html'
    recordset = {}
    system = {}
    region = {}
    node1 = None
    node2 = None
    rel = ''
    result = {}
    result1 = {}
    extra = False

    try:
        recordset = graph.run('Match (n:RecordSet) Return n.name,n.id').data()
        system = graph.run('Match (n:System) Return n.name,n.id').data()
        region = graph.run('Match (n:Region) Return n.name,n.id').data()
    except:
        print('No data from database')

    if request.method == 'GET':
        # print(request.GET)
        if request.GET.get('choose1') != '':
            if request.GET.get('choose5') != '':
                if request.GET.get('choose7') != '':
                    node1 = request.GET.get('choose1')
                    node2 = request.GET.get('choose5')
                    rel = request.GET.get('choose7')
        elif request.GET.get('choose2') != '':
            if request.GET.get('choose4') != '':
                if request.GET.get('choose7') != '':
                    node1 = request.GET.get('choose2')
                    node2 = request.GET.get('choose4')
                    rel = request.GET.get('choose7')
                    print('bbb')
            elif request.GET.get('choose5') != '':
                if request.GET.get('choose8') != '':
                    node1 = request.GET.get('choose2')
                    node2 = request.GET.get('choose5')
                    rel = request.GET.get('choose8')
            elif request.GET.get('choose6') != '':
                if request.GET.get('choose9') != '':
                    node1 = request.GET.get('choose2')
                    node2 = request.GET.get('choose6')
                    rel = request.GET.get('choose9')
        elif request.GET.get('choose3') != '':
            if request.GET.get('choose5') != '':
                if request.GET.get('choose9') != '':
                    node1 = request.GET.get('choose3')
                    node2 = request.GET.get('choose5')
                    rel = request.GET.get('choose9')

    ## one_bidirection

    if node1 != None and node2 != None and rel != None and 'create' in request.GET:
        data1 = ast.literal_eval(node1)
        query = "Match (n)where n.name='{}' AND n.id='{}' return n".format(data1['n.name'], data1['n.id'])
        Node1 = graph.run(query).to_subgraph()
        # print(query)
        data2 = ast.literal_eval(node2)
        query = "Match (n)where n.name='{}' AND n.id='{}' return n".format(data2['n.name'], data2['n.id'])
        Node2 = graph.run(query).to_subgraph()
        # print(query)
        if request.GET.get('one_bidirection') != 'on':
            try:
                graph.create(Relationship(Node1, rel, Node2))
                result = graph.run('Match {}-[r:{}]->{} Return r limit 5'.format(Node1, rel, Node2)).to_table()
            except:
                print('error')
        else:
            try:
                graph.create(Relationship(Node1, rel, Node2))
                graph.create(Relationship(Node2, rel, Node1))
                result = graph.run('Match (n)-[r:{}]-(m) Return n ,r, m limit 5'.format(rel)).to_table()
            except:
                print('error')

    elif node1 != None and node2 != None and rel != None and 'delete' in request.GET:
        data1 = ast.literal_eval(node1)
        query = "Match (n)where n.name='{}' AND n.id='{}' return n".format(data1['n.name'], data1['n.id'])
        Node1 = graph.run(query).to_subgraph()
        # print(query)
        data2 = ast.literal_eval(node2)
        query = "Match (n)where n.name='{}' AND n.id='{}' return n".format(data2['n.name'], data2['n.id'])
        Node2 = graph.run(query).to_subgraph()
        # print(query)
        if request.GET.get('one_bidirection') != 'on':
            try:
                graph.run("Match {}-[r:{}]-{} delete r ".format(Node1, rel, Node2))
            except:
                print('error')
        else:
            try:
                graph.run("Match {}-[r:{}]-{} delete r ".format(Node1, rel, Node2))
                graph.run("Match {}-[r:{}]-{} delete r ".format(Node2, rel, Node1))
            except:
                print('error')

    context = {'recordset': recordset,
               'system': system,
               'region': region,
               'result': result,
               'result1': result1,
               'extra': extra,
               }
    return render(request, template, context)


