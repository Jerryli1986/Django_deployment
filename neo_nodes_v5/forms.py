from django import forms
from .models import *

class RecordSetForm(forms.ModelForm):
    class Meta:
        model=RecordSet
        fields = '__all__'


class RegionForm(forms.ModelForm):
    class Meta:
        model=Region
        fields = '__all__'


class SystemForm(forms.ModelForm):
    class Meta:
        model=System
        fields = '__all__'

        # REGION_CHOICES = {('EMEA', 'EMEA'),
        #                   ('AMER', 'AMER'),
        #                   ('APAC', 'APAC')
        #                   }
        # BUSINESSES_CHOICES = {('Equities', 'Equities'),
        #                       ('Fixed Income', 'Fixed Income'),
        #                       ('Foreign Exchange', 'Foreign Exchange'),
        #                       ('Derivatives', 'Derivatives')
        #                       }

        # regions = forms.MultipleChoiceField(choices=REGION_CHOICES, widget=forms.CheckboxSelectMultiple())
        # businesses=forms.MultipleChoiceField(choices=BUSINESSES_CHOICES, widget=forms.CheckboxSelectMultiple())




class RelationshipsForm(forms.ModelForm):
    class Meta:
        model=Relationships
        fields = {'rel_properties'}

