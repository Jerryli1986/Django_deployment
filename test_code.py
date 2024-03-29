from py2neo import Graph
import ast
import pandas
from py2neo import Node, Relationship,Subgraph,NodeMatcher
from py2neo.ogm import GraphObject,Property
#from scripts.vis import draw
graph=Graph("bolt://127.0.0.1:7687",auth=("neo4j","password"))
#graph = Graph("http://neo4j:password@localhost:7474")
#graph.delete_all()

# nicole = Node("Per", name="Nicole", age=24)
# graph.create(nicole)

# matcher = NodeMatcher(graph)
# print(list(matcher.match('dDs')))

# matcher = NodeMatcher(graph)
# print(matcher.match('city'))
# nicole=Node("Per", name="Nicole", age=24,gender='M')
# graph.merge(nicole,'Per','gender')


# drew = Node("Person", name="Drew", age=20)
#
# mtdew = Node("Drink", name="Mountain Dew", calories=9000)
# cokezero = Node("Drink", name="Coke Zero", calories=0)
#
# coke = Node("Manufacturer", name="Coca Cola")
# pepsi = Node("Manufacturer", name="Pepsi")
#
# graph.create(nicole | drew | mtdew | cokezero | coke | pepsi)
# graph.create( mtdew | cokezero  )
#
#
# ## create the relationship
# ab=graph.create(Relationship(mtdew,'BelongTo',cokezero))


# MATCH (n) DETACH DELETE n

# MATCH (a:Drink{name:'Coke Zero'}),(b:Drink { name: 'Mountain Dew' })
# MERGE (a)-[r:KNOWS]-(b)
# RETURN r

# query=" MATCH {}, {} MERGE {}-[r:{}]->{}".format(mtdew, cokezero,mtdew, 'Sell', cokezero)
# graph.run(query)
##################################
# query1="Match (n)where n.name='{}' AND n.calories={} return n".format("Mountain Dew",9000)
# print(query1)
# N1=graph.run(query1).to_subgraph()
#
# query2="Match (n)where n.name='{}' AND n.calories={} return n".format("Coke Zero",0)
# print(query2)
# N2=graph.run(query2).to_subgraph()
#
# # query=" MATCH {}, {} MERGE {}-[r:{}]->{}".format(N1, N2, N1, 'Sell', N2)
# # print(query)
# # graph.run(query)
#
# graph.create(Relationship(N1,"Sell",N2))
#################################
# match (n:Drink{
#   name: "Mountain Dew",
#   calories: 9000
# }) -[r:Sell]-(m:Drink{
#   name: "Coke Zero",
#   calories: 0
# }) delete r
#################################
# Match (n:Person{name: "Keanu Reeves",born: 1964})-[r]-(m:Person{name: "Carrie-Anne Moss", born: 1967}) return n,m
#####################################
# MATCH (a:Drink),(b:Drink)
# WHERE a.name = 'Mountain Dew' AND b.name = 'Coke Zero'
# CREATE (a)-[r:Likes { name: a.name + '<->' + b.name }]->(b)
# RETURN a,b


# mc=graph.merge(mtdew,'Drink','name')
# dd=graph.merge(mtdew)
# print(Relationship(mtdew, "KNOWS", cokezero))
# graph.create(Relationship(nicole, "LIKES", mtdew))
# graph.create(Relationship(drew, "LIKES", mtdew))
# graph.create(Relationship(coke, "MAKES", cokezero))
# graph.create(Relationship(pepsi, "MAKES", mtdew))
#
#
# query = """
# MATCH (person:Person)-[:LIKES]->(drink:Drink)
# RETURN person.name AS name, drink.name AS drink
# """

# query = """
# MATCH (n:System)
# RETURN n
# """
# create node with parameter of property
# CREATE (n:Person $props)
# RETURN n


# pin install panda
# data = graph.run(query).to_data_frame()

# data = graph.run(query)
import json

# data=graph.run('Match (n:Region) Return n').to_data_frame()
#
#
#
# # print(type(data))
# # print(data)
# # print(pandas.DataFrame(data))
# cc=pandas.DataFrame(data)
# print(cc['n'][0])
# for d in cc['n'].values:
#     print (d)


# data=(graph.run('Match (n:Region) Return n.name,n.id').data())
# print(data)
# # print(type(data))
# # for d in data:
# #     print(type(d))
# #     print (d['n.name'],d['n.id'])


# data=(graph.run('Match (n:Region) Return n.name,n.id').data())
# # print(data)
# # print(type(data))
# for d in data:
#     print(d.values())
    # print (d['n.name'],d['n.id'])


# data=(graph.run('Match (n:Region) Return n.name,n.id').data())
# print(data)
# # print(type(data))
# for d in data:
#      print(d)
# conver str to dict
# ss=ast.literal_eval(str_dict)
#           print(type(ss))
#           print(ss['n.name'])


# print(type(data))
# cc=pandas.DataFrame(data)
# print(cc['n'][0])
# data.T
# for d in data:
#     print(type(d))
#     print (d['n.name'],d['n.id'])




####
#'Let\'s learn Python'
# "Let's learn Python"

# # """
# """
# this is a tuorial
# on Python
# """
#
# 'This is a tutorial\non Python\n'
# ####

# def test_var_args(f_arg, *argv):
#     print("first normal arg:", f_arg)
#     for arg in argv:
#         print("another arg through *argv :", arg)
#
#
# def greet_me(**kwargs):
#     if kwargs is not None:
#         for key, value in kwargs.items():
#             print("%s = %s" % (key, value))
#
#
# argv=('python', 'eggs', 'test')
# # test_var_args('yasoob',*argv )
# kwargs={'name':'jerry','gender':'M','city':'London'}
# # greet_me(**kwargs)


# class1=type(str(class_name),*argv,**kwargs)

# ##################################################################
# class BaseClass(GraphObject):
#     def __init__(self,classtype):
#         self._type=classtype

## create dynamic class
# def ClassFactory(name, argnames, BaseClass=BaseClass):
#     def __init__(self, **kwargs):
#         for key, value in kwargs.items():
#             # here, the argnames variable is the one passed to the
#             # ClassFactory call
#             if key not in argnames:
#                 raise TypeError("Argument %s not valid for %s"
#                     % (key, self.__class__.__name__))
#             setattr(self, key, value)
#         BaseClass.__init__(self, name[:-len("Class")])
#     newclass = type(name, (BaseClass,),{"__init__": __init__})
#     return newclass
# >>> SpecialClass = ClassFactory("SpecialClass", "a b c".split())
# >>> s = SpecialClass(a=2)
######################################################################
# dynamic args in class

# class Test:
#     def __init__(self, *args, **kwargs):
#         self.args=dict(**kwargs)
#
#     def getkwargs(self):
#         print(self.args)
#
# t=Test(a=1, b=2, c="cats")
# t.getkwargs()

####################################################
# class Var:
#     def __init__(self,**kwargs):
#         for attr in kwargs.keys():
#             self.__dict__[attr] = kwargs[attr]
#
# v = Var(name="Sam",age=22)

##############################################################

# class BaseClass(GraphObject):
#     def __init__(self):
#         self._type=Property()
#
# def ClassFactory(name,arguments,BaseClass=BaseClass):
#     def __init__(self,**kwargs):
#         for key, value in kwargs.items():
#             self.__dict__[key]=Property()
#             if key in arguments :
#                 setattr(self, key, value)
#             else:
#                 raise TypeError("Argument %s not valid for %s" % (key, self.__class__.__name__))
#         BaseClass.__init__(self)
#     newclass = type(name, (BaseClass,),{"__init__": __init__})
#     return newclass
#
# arguments=["name","gender","age"]
# class_name='People'
# People=ClassFactory(class_name,arguments)
#
# a=People(name='jerry')
# print(a.name)


# a='abcde'
# att_dict={str(a): 123,'cdde':3344443}
# graph.create(Node('AAA', **att_dict))




###########################
# class Myclass:
#
#     def __init__(self, **kwargs):
#         # all those keys will be initialized as class attributes
#         allowed_keys = set(['attr1','attr2','attr3'])
#         # initialize all allowed keys to false
#         self.__dict__.update((key, False) for key in allowed_keys)
#         # and update the given keys by their given values
#         self.__dict__.update((key, value) for key, value in kwargs.items() if key in allowed_keys)


# a=[{'a':1,'b':2}]
# print(a[0].items())

# for k,v in a[0].items():
#     print (k)
#     print(v)
#     print ({k:v})
#
# b={'attr_name': 'AFDAS', 'attr_value': 'FAF', 'id': None}
#
# print(b.values)


########json########
# import json
#
# # a Python object (dict):
# x = {
#   "name": "John",
#   "age": 30,
#   "city": "New York"
# }
#
# # convert into JSON:
# y = json.dumps(x)
#
# # the result is a JSON string:
# print(y)

##########################
# a={'a1':123,'b1':234}
# print ( a.keys())

#########

# class People:
#     abc=123
#     def __init__(self,conn):
#         self.conn=conn
#     def returnobject(self):
#         return self
#
#
# a=People('sql')
# b=a.returnobject()
# print(type(b))
# print(b)

########csv
# import os
# file_path="C:\\Users\\jerryzli\\Downloads"
# print(file_path)
# table_parsed = os.path.join(file_path,'test.csv' )
# with open(table_parsed, 'r') as f:
#     print(f)
#     count = sum(1 for line in f) - 1
# print(count)

###############csv  with  'utf-8' codec can't decode byte 0xae

# import os
# file_path="C:\\Users\\jerryzli\\Downloads"
# print(file_path)
# table_parsed = os.path.join(file_path,'test.csv' )
# with open(table_parsed, 'r',errors='ignore') as f:
#     print(f)
#     count = sum(1 for line in f) - 1
# print(count)

#######################################
# result=zip(['abc','bcd'],[1,2])
# # Converting itertor to set
# resultSet = set(result)
# print(resultSet)
#
# result=zip(['abc','bcd'],[1,2])
# # Converting itertor to dict
# resultDict = dict(result)
# print(resultDict)


######
# result=zip(['abc','bcd'],[1,2])
# # Converting itertor to dict
# resultDict = dict(result)
# # Converting dict to tuple
# print(tuple(resultDict))

# creating a tuple from a dictionary
# t1 = tuple({1: 'one', 2: 'two'})
# print('t1=',t1)

########pop()####

# a=['a','b','c']
# a.pop(-1)
# print(a)

# a=['a','b','c']
# direction=0
# a.pop(direction)
# print(a)

#####zipfile module###
#links: https://www.geeksforgeeks.org/working-zip-files-python/
# from zipfile import ZipFile
# import os
# output=None
# file_name=r"C:\Users\jerryzli\Downloads\transport-network.zip"
# with ZipFile(file_name, mode='r') as zf:
#     # printing all the contents of the zip file
#     zf.printdir()
#
#     # extracting all the files
#     print('Extracting all the files now...')
#     ##extractall() method will extract all the contents of the zip file to the current working directory
#     output_dir=r"C:\Users\jerryzli\Downloads\transport-network_copy"
#     os.mkdir(output_dir)
#     zf.extractall(path=output_dir)
#
#     print('Done!')


#################### parser
#
# def text_parser(document):
#     fpath = document['dst_file_path']
#     #encoding = document['file_encoding'].split('=')[1]
#     encoding = document['file_encoding']
#     d = {'deloitte_meta': document, }
#
#     with open(fpath, 'r', encoding=encoding) as fin:
#         data = fin.read()
#
#     if data is None:
#         data = ''
#     d['content'] = data
#     print(d)
#     return d
# document={'dst_file_path':r"C:\Users\jerryzli\Downloads\test_python.txt"
#            ,'file_encoding':"UTF-8"}
# text_parser(document)

#################################################

# from tika import parser
# def tika_parser(document):
#     # Parse document with tika
#     fpath = document['dst_file_path']
#     d = parser.from_file(fpath, xmlContent=True)
#     # print(d)
#     if 'content' not in d or d['content'] is None:
#         raise Exception('File is PasswordProtected, Empty or not supported by TIKA')
#
#     # Create parsed doc to index into cluster
#     parsed_doc = {}
#     parsed_doc['deloitte_meta'] = document
#     parsed_doc['content'] = d['content']
#
#     # Pull specific metadata out and lump the rest into a single string
#     heads = ['Author', 'Content-Type', 'meta:save-date', 'Creation-Date']
#     specific_meta= {}
#
#     for head in heads:
#         if head in d['metadata']:
#             specific_meta[head] = d['metadata'][head]
#         elif head == 'meta:save-date' or head == 'Creation-Date':
#             specific_meta[head] = "1900-01-01T00:00:00.000Z"
#         else:
#             specific_meta[head] = ''
#
#     specific_meta['tika_metadata'] = str(d['metadata'])
#     parsed_doc['metadata'] = specific_meta
#     print(specific_meta)
#     return parsed_doc
#
# document={'dst_file_path':r"C:\Users\jerryzli\Downloads\transport-network.zip"
#            ,'file_encoding':"UTF-8",}
# tika_parser(document)

##############################################################
#########collections.Counter()################
#links: https://www.pythonforbeginners.com/collection/python-collections-counter
# import collections
# cnt = collections.Counter()
# wordslist=['red', 'blue', 'red', 'green', 'blue', 'blue']
# wordsdict={'red':2, 'blue':3}
#
# ### this is update cnt
# # for word in wordslist:
# #     cnt[word]+=1
# # print(cnt)
#
# ## another way to update cnt
# cnt.update(wordslist)
# print(cnt)

####
# cnt1=collections.Counter(wordslist)
# cnt2=collections.Counter(wordsdict)
# cnt3=collections.Counter(a=2,b=4,c=6)
# print(cnt1)
# print(cnt2)
# print(cnt3)

#########################
import hashlib

#Constructors for hash algorithms sha1(), sha224(), sha256(), sha384(), sha512(), blake2b(), and blake2s(). md5()
# m=hashlib.sha256()
# # m=hashlib.md5()
# m.update(b"Nobody inspects")
# print(m.hexdigest())
# #####
# n=hashlib.md5(b"Nobody inspects").hexdigest()
# print(n)
#######################################################
#### this is not finished have error
# import magic
# def _get_mime(self, binary_buffer):
# 	# expects a file to be opened in binary and read
# 	m = magic.Magic()
# 	print( m.from_buffer(binary_buffer).split('; '))
#
# fpath=r'C:\Users\jerryzli\Desktop\DUST_stuff\collection_table_list.txt'
# with open(fpath, 'rb') as fin:
# 	buff = fin.read()
# print(buff)
# _get_mime(buff)

##########replace

# a={'path':'/acb/bcd.ext','name':'good'}
# c=a['path'].replace('ext','eee')
# print(c)
# print(a)

#################
#
# import os
#
# fpath = r'C:\Users\jerryzli\Desktop\DUST_stuff'
# fpath1 = r'C:\Users\jerryzli\Desktop\DUST_stuff\collection_table_list.txt'
# print(os.path.isdir(fpath1))
# print(os.path.isfile(fpath))
#
#
# def get_safe_dir(path):
# 	if os.path.exists(path) and not os.path.isdir(path):
# 		msg = 'path must be a directory: {0}'
# 		raise TypeError(msg.format(path))
#
# 	if os.path.isdir(path):
# 		# split the path, we may have already inserted
# 		# an underscore to this path
# 		split = path.split('_')
# 		print(split)            # ['C:\\Users\\jerryzli\\Desktop\\DUST', 'stuff']
# 		try:
# 			n = int(split[-1])
# 			split[-1] = str(n + 1)
# 		except:
# 			n = 1
# 			split.append(str(n))
#
# 		path = '_'.join(split)
# 		print(path)
# 		# make sure this new directory is safe
# 		return get_safe_dir(path)
#
# 	return path
#
# get_safe_dir(fpath)
#####################################
# a={1,2}
# b=[5,44]
# c=object
# print(a,b,c)
# {1, 2} [5, 44] <class 'object'>
############################
# import os
# fpath1 = r'C:\Users\jerryzli\Desktop\DUST_stuff\collection_table_list.txt'
# print(os.path.splitext(fpath1))
#('C:\\Users\\jerryzli\\Desktop\\DUST_stuff\\collection_table_list', '.txt')


#####
# class People:
#
#     def __init__(self,name,age):
#         self.name=name
#         self.age=age
#
#
# jerry=People('jerry',30)
#
# print(jerry.__dict__)

########parser
# import configparser
# parser = configparser.ConfigParser()
# _run_cfg = r'C:\Users\jerryzli\Desktop\AFT-000018.cfg'
# parser.read(_run_cfg)
# print('parser:' ,parser.__dict__)
# print('parser:' ,parser['meta-db'].__dict__)


############
import os
fpath=r'C:\Users\jerryzli\Desktop\AFT-000018.cfg'
dir_=os.scandir(r'C:\Users\jerryzli\Desktop')
for d in dir_:
    print (d)
##result##########
# <DirEntry 'AFT-000018.cfg'>
# <DirEntry 'Atom.lnk'>
# <DirEntry 'desktop.ini'>
# <DirEntry 'Downloads - Shortcut.lnk'>
# <DirEntry 'DUST_stuff'>
# <DirEntry 'personal'>
# <DirEntry 'Python_Django_Udemy_Training'>
###############