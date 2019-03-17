from django.db import models

from py2neo import Graph,Node,NodeMatcher,Relationship
from py2neo.ogm import GraphObject,Property
from Test2_py2neo.settings import graph

class Label(models.Model):
    label=models.CharField(max_length=100)
    def __str__(self):
        return self.label

class Attribute(models.Model):
      label_name=models.ForeignKey(Label,on_delete=models.CASCADE)
      attr_name=models.CharField(max_length=100)
      attr_value=models.CharField(max_length=100)
      def __str__(self):
          return self.attr_name












#
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

# arguments=["name","gender","age"]
# class_name='People'
# People=ClassFactory(class_name,arguments)

# a=People(name='jerry')
# print(a.name)

