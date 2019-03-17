from django.db import models

from py2neo import Graph,Node,NodeMatcher,Relationship
from py2neo.ogm import GraphObject,Property


# pip install django-multiselectfield
# from multiselectfield import MultiSelectField





class RecordSet(models.Model):
    NAME_CHOICES={('Customer Details','Customer Details'),
               ('Trades','Trades'),
               ('Orders','Orders'),
               ('Settlements','Settlements')
               }
    FORMAT_CHOICES  = {('Database record', 'Database record'),
                       ('Archive record', 'Archive record')
                       }

    name = models.CharField(max_length=266, choices=NAME_CHOICES, null=True, blank=True)
    id = models.CharField(max_length=266,primary_key=True)
    dataContactEmail= models.EmailField(blank=True,null=True)
    dataContactName = models.CharField(max_length=266,blank=True,null=True)
    EpochFrom       = models.CharField(max_length=266,blank=True,null=True)
    format          = models.CharField(max_length=266,choices=FORMAT_CHOICES,null=True,blank=True)
    availableFrom   = models.CharField(max_length=266,blank=True,null=True)
    availableTo     = models.CharField(max_length=266,blank=True,null=True)
    businessContactPhone = models.CharField(max_length=266)
    EpochTo              = models.CharField(max_length=266,blank=True,null=True)
    businessContactEmail = models.EmailField(blank=True,null=True)
    dataContactPhone     = models.CharField(max_length=266,blank=True,null=True)
    businessContactName  = models.CharField(max_length=266,blank=True)
    extractionSLA        = models.CharField(max_length=266,blank=True)

    def __str__(self):
        return str(self.name)


class Region(models.Model):
    NAME_CHOICES={('EMEA','EMEA'),('AMER','AMER'),('APAC','APAC')}

    name        = models.CharField(max_length=266,choices=NAME_CHOICES)
    id          = models.CharField(max_length=266,primary_key=True)
    def __str__(self):
        return str(self.name)

class System(models.Model):
    REGION_CHOICES={('EMEA','EMEA'),
                    ('AMER','AMER'),
                    ('APAC','APAC')
                    }
    BUSINESSES_CHOICES={('Equities','Equities'),
                        ('Fixed Income','Fixed Income'),
                        ('Foreign Exchange','Foreign Exchange'),
                        ('Derivatives','Derivatives')
                        }
    name            =models.CharField(max_length=266)
    ownerPhoneNumber=models.CharField(max_length=266,blank=True)
    regions         = models.CharField(max_length=266)
    #regions        =MultiSelectField(REGION_CHOICES)
    ownerName       =models.CharField(max_length=266,blank=True)
    id              =models.CharField(max_length=266,primary_key=True)
    businesses      =models.CharField(max_length=266)
    # businesses      =MultiSelectField(BUSINESSES_CHOICES)
    ownerEmail      =models.EmailField(blank=True,null=True)

    def __str__(self):
        return str(self.name)



class Label(models.Model):

    LABEL_CHOICES={('RecordSet','RecordSet'),
                   ('Region','Region'),
                   ('System','System')}

    label=models.CharField(max_length=266,choices=LABEL_CHOICES )


    def __str__(self):
        return str(self.label)


class Relationships(models.Model):
    node1=models.CharField(max_length=266)
    node2=models.CharField(max_length=266)
    rel  =models.CharField(max_length=266)
    one_two_direction=models.BooleanField(default=False)   # False mean single
    rel_properties=models.CharField(max_length=266)

    def one_2_two(self):
        self.one_two_direction = True
        self.save()
