from django import forms
from .models import *


class LabelForm(forms.ModelForm):
    class Meta:
        model=Label
        fields='__all__'
        labels = {
            'label': 'Choose Label:',
        }


class RecordSetForm(forms.ModelForm):
    class Meta:
        model=RecordSet
        exclude =['EpochFrom','EpochTo']


class RegionForm(forms.ModelForm):
    class Meta:
        model=Region
        fields = '__all__'



class SystemForm(forms.ModelForm):
    regions = forms.ModelMultipleChoiceField(queryset=None)
    businesses = forms.ModelMultipleChoiceField(queryset=None,
                                                widget=forms.CheckboxSelectMultiple())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['regions'].queryset =Region.objects.all() # pre create Region object in admin
        self.fields['businesses'].queryset = Business.objects.all()  # pre create Region object in admin
    class Meta:
        model=System
        fields='__all__'
        # widgets = {
        #     'regious': forms.CheckboxSelectMultiple(),
        # }
class RelationshipsForm(forms.ModelForm):
    CHOICES={('System->RecordSet',(11,'Contains')),
              ('System->System',((21,'Trades'),
                                 (22,'Settlements'),
                                 (23,'CustomerDetails'),
                                 (24,'Orders'))),
             ('System->Region',(31,'UseIn'))
             }
    name = forms.ChoiceField(choices=CHOICES)
    one_bidirection=forms.BooleanField(widget=forms.CheckboxInput())

    class Meta:
        model=Relationships
        fields = '__all__'

