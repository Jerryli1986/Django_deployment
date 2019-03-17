from django.db import models
from py2neo import Graph,Node,NodeMatcher,Relationship
from py2neo.ogm import GraphObject,Property
from Test2_py2neo.settings import graph

#graph=Graph("bolt://127.0.0.1:7687",auth=("neo4j","password"))

class Register(GraphObject):

    name = Property()
    gender  = Property()

    def __unicode__(self):
        return u"%s" % (self.name)

    # def add_register (self):
    #     If_exists_1=NodeMatcher(graph).match(self,Register,self.name).first()
    #     if not If_exists_1 :
    #         register=Node(self,Register,name=self.name,gender=self.gender)
    #         graph.create(register)
    #         return True
    #     else:
    #         return False

class Country(GraphObject):

        country_name = Property()
        population=Property()

        def __unicode__(self):
            return u"%s" % (self.country_name)

        # def add_country(self):
        #     If_exists_2 = NodeMatcher(graph).match(self, Country, self.country_name).first()
        #     if not If_exists_2:
        #         country = Node(self,Country, country_name=self.country_name, population=self.population)
        #         graph.create(country)
        #         return True
        #     else:
        #         return False
        #
        # def add_relationship(self):
        #     rel=Relationship(Register,'LIVED_IN',self)
        #     graph.create(rel)


##### SQLite
class Register_SQL(models.Model):

    name = models.CharField(max_length=100)
    gender  = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Country_SQL(models.Model):
    country_name = models.CharField(max_length=100)
    population  = models.FloatField()

    def __str__(self):
        return self.country_name
