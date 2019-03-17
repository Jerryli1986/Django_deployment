from django import forms
from .models import *


class LabelForm(forms.ModelForm):
    class Meta:
        model=Label
        fields=['label',
                ]

        labels={'label':'Label',
                }

class AttributeForm(forms.ModelForm):
    class Meta:
        model=Attribute
        fields = ['attr_name',
                  'attr_value'
                  ]

        widgets = {
            'attr_name':forms.TextInput(attrs={'class':'formset-field'}),
            'attr_value': forms.TextInput(attrs={'class': 'formset-field'}),
                  }


class QueryForm(forms.Form):
    query_=forms.CharField(max_length=100)