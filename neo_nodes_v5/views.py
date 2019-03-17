
# nodes views.py
import pandas as pd
import re
import json
import json as simplejson
from django.http import HttpResponse
import ast
from django.shortcuts import render
from .forms import *
from .models import System,RecordSet,Region
from py2neo import Database,Graph, Node, Relationship
graph=Graph("bolt://127.0.0.1:7687",auth=("neo4j","neo4j2"))


def index(request):
    template='neo_nodes_v5/base.html'
    return render(request, template )

# def get_data_list(Classname,*args,**kwargs):
#     name_list=Classname.objects.orderby('name')
#     return name_list

def add_nodes(request):
        context = {}
        properties = {}
        RecordSet_form= RecordSetForm(request.POST or None)
        Region_form = RegionForm(request.POST or None)
        System_form = SystemForm(request.POST or None)
        if request.method == "POST" and "Record_create" in request.POST :
            form=RecordSet_form

            if form.is_valid():
                form.save()
                #print(form.cleaned_data.get('name'))
                label = form.__class__.Meta.model.__name__
                properties = form.cleaned_data
                print(properties)
                graph.create(Node(label, **properties))
        elif request.method == "POST" and "Region_create" in request.POST :
            form = Region_form

            if form.is_valid():
                form.save()
                label = form.__class__.Meta.model.__name__
                print(label)
                properties = form.cleaned_data

                graph.create(Node(label, **properties))
        elif request.method == "POST" and "System_create" in request.POST:
            form = System_form
            if form.is_valid():
                form.save()
                label = form.__class__.Meta.model.__name__
                properties = form.cleaned_data
                graph.create(Node(label, **properties))

        context = {
            'form_recordset':RecordSet_form,
            'form_region': Region_form,
            'form_system': System_form,
            'node':properties,
        }
        template = 'neo_nodes_v5/nodes_create.html'
        return render(request, template , context)


# select from database
def select_nodes(request):
   template='neo_nodes_v5/edges_create.html'
   recordset = {}
   system = {}
   region = {}
   node1=None
   node2=None
   rel=''
   result ={}
   result1={}
   extra=False
   # label=Label.objects.all()

   # recordset=RecordSet.objects.all()
   # system = System.objects.all()
   # region = Region.objects.all()
   try:
       # recordset = graph.run('Match (n:RecordSet) Return n.name').to_data_frame()['n.name']
       # system = graph.run('Match (n:System) Return n.name').to_data_frame()['n.name']
       # region = graph.run('Match (n:Region) Return n.name').to_data_frame()['n.name']
       recordset = graph.run('Match (n:RecordSet) Return n.name,n.id').data()
       system = graph.run('Match (n:System) Return n.name,n.id').data()
       region = graph.run('Match (n:Region) Return n.name,n.id').data()

   except :
       print('No data from database')


   # print(request.GET)
   if request.method=='GET':
       # print(request.GET)
       if request.GET.get('choose1') !='':
           if request.GET.get('choose5') !='':
               if request.GET.get('choose7') !='' :
                   node1 = request.GET.get('choose1')
                   node2 = request.GET.get('choose5')
                   rel  =  request.GET.get('choose7')
       elif request.GET.get('choose2') !='':
                   if request.GET.get('choose4') !='':
                       if request.GET.get('choose7') !='':
                           node1 = request.GET.get('choose2')
                           node2 = request.GET.get('choose4')
                           rel = request.GET.get('choose7')
                           print('bbb')
                   elif request.GET.get('choose5') !='':
                       if request.GET.get('choose8') !='':
                           node1 = request.GET.get('choose2')
                           node2 = request.GET.get('choose5')
                           rel = request.GET.get('choose8')
                   elif request.GET.get('choose6') !='':
                       if request.GET.get('choose9') !='':
                           node1 = request.GET.get('choose2')
                           node2 = request.GET.get('choose6')
                           rel = request.GET.get('choose9')
       elif request.GET.get('choose3') !='' :
           if request.GET.get('choose5') !='':
               if request.GET.get('choose9') !='' :
                   node1 = request.GET.get('choose3')
                   node2 = request.GET.get('choose5')
                   rel = request.GET.get('choose9')

    ## one_bidirection

   if node1 !=None and node2 != None and rel != None and 'create' in request.GET:
        data1=ast.literal_eval(node1)
        query="Match (n)where n.name='{}' AND n.id='{}' return n".format(data1['n.name'],data1['n.id'])
        Node1=graph.run(query).to_subgraph()
        # print(query)
        data2 = ast.literal_eval(node2)
        query = "Match (n)where n.name='{}' AND n.id='{}' return n".format(data2['n.name'], data2['n.id'])
        Node2 = graph.run(query).to_subgraph()
        # print(query)
        if request.GET.get('one_bidirection') != 'on':
            try:
               graph.create(Relationship(Node1, rel, Node2))
               result = graph.run('Match {}-[r:{}]->{} Return r limit 5'.format(Node1,rel,Node2)).to_table()
            except:
                print('error')
        else:
            try:
                graph.create(Relationship(Node1, rel, Node2))
                graph.create(Relationship(Node2, rel, Node1))
                result = graph.run('Match (n)-[r:{}]-(m) Return n ,r, m limit 5'.format(rel)).to_table()
            except:
                print('error')
        ## display

   # elif node1 !=None and node2 != None and rel != None and 'search' in request.GET:
   #     data1 = ast.literal_eval(node1)
   #     query = "Match (n)where n.name='{}' AND n.id='{}' return n".format(data1['n.name'], data1['n.id'])
   #     Node1 = graph.run(query).to_subgraph()
   #     # print(query)
   #     data2 = ast.literal_eval(node2)
   #     query = "Match (n)where n.name='{}' AND n.id='{}' return n".format(data2['n.name'], data2['n.id'])
   #     Node2 = graph.run(query).to_subgraph()
   #     # print(query)
   #     if request.GET.get('one_bidirection') != 'on':
   #         try:
   #             print("Match {}-[r]-{}".format(Node1, Node2))
   #             result=graph.run("Match {}-[r]-{}".format(Node1,Node2)).to_table()
   #
   #         except:
   #             print('error')
   #     else:
   #         try:
   #             result=graph.run("Match {}-[r]-{}".format(Node1,Node2)).to_table()
   #             result1=graph.run("Match {}-[r]-{}".format(Node2, Node1)).to_table()
   #             extra=True
   #
   #         except:
   #             print('error')

   # elif rel != None and 'search' in request.GET:
   #         try:
   #             print("Match (n)-[r:{}]-(m)".format(rel))
   #             result=graph.run("Match (n)-[r:{}]-(m)".format(rel)).to_table()
   #
   #         except:
   #             print('error')
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
               graph.run("Match {}-[r:{}]-{} delete r ".format(Node1,rel, Node2))
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

























# def get_list(request):
#
#     answer=request.GET['lb']
#     print(answer)
#     select_list=get_data_list(answer)
#     result_set=[]
#     for node in select_list:
#         result_set.append({'name': node.name})
#     return HttpResponse(simplejson.dumps(result_set), mimetype='application/json', content_type='application/json')
#


