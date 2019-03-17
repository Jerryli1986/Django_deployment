from django.db import models
import time

class Label(models.Model):
    LABEL_CHOICES={('RecordSet','RecordSet'),
                   ('Region','Region'),
                   ('System','System')}

    label=models.CharField(max_length=266,choices=LABEL_CHOICES )

    def __str__(self):
        return str(self.label)

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
    format          = models.CharField(max_length=266,choices=FORMAT_CHOICES,null=True,blank=True)
    availableFrom   = models.CharField(max_length=266,blank=True,null=True)
    availableTo     = models.CharField(max_length=266,blank=True,null=True)
    businessContactPhone = models.CharField(max_length=266)
    EpochFrom            = models.CharField(max_length=266, blank=True, null=True)
    EpochTo              = models.CharField(max_length=266,blank=True,null=True)
    businessContactEmail = models.EmailField(blank=True,null=True)
    dataContactPhone     = models.CharField(max_length=266,blank=True,null=True)
    businessContactName  = models.CharField(max_length=266,blank=True)
    extractionSLA        = models.CharField(max_length=266,blank=True)

    def datatoEpoch(self,inputdate):
        pattern = '%Y-%m-%d'
        epoch = int(time.mktime(time.strptime(inputdate, pattern)))
        return epoch

    def __str__(self):
        return str(self.name)


class Region(models.Model):
    NAME_CHOICES={('EMEA','EMEA'),
                  ('AMER','AMER'),
                  ('APAC','APAC')}
    name        = models.CharField(max_length=266,choices=NAME_CHOICES)
    id          = models.CharField(max_length=266,primary_key=True)

    def get_id(self):
        if self.name=='EMEA' :
            id='R1'
        elif self.name=='AMER' :
            id='R2'
        elif self.name=='APAC' :
            id='R3'
        else:
            id='Other'
    def __str__(self):
        return str(self.name)

class System(models.Model):
    name            =models.CharField(max_length=266)
    ownerPhoneNumber=models.CharField(max_length=266,blank=True)
    regions         = models.CharField(max_length=266,blank=True)
    ownerName       =models.CharField(max_length=266,blank=True)
    id              =models.CharField(max_length=266,primary_key=True)
    businesses      =models.CharField(max_length=266,blank=True)
    ownerEmail      =models.EmailField(blank=True,null=True)

    def __str__(self):
        return str(self.name)

class Business(models.Model):
    BUSINESSES_CHOICES = {('Equities', 'Equities'),
                          ('Fixed Income', 'Fixed Income'),
                          ('Foreign Exchange', 'Foreign Exchange'),
                          ('Derivatives', 'Derivatives')
                          }
    name=models.CharField(max_length=266,choices=BUSINESSES_CHOICES)
    def __str__(self):
        return str(self.name)


class Relationships(models.Model):
    name=models.CharField(max_length=266)
    one_bidirection=models.BooleanField(default=False)   # False mean single
    rel_properties=models.CharField(max_length=266,blank=True)

    def __str__(self):
        return str(self.name)

