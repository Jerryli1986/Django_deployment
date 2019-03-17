from django import forms
from .models import *


class NodeIdForm(forms.ModelForm):
    class Meta:
        model=NodeId
        fields=['node_id',
                ]

        labels={'node_id':'NodeId',
                }


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