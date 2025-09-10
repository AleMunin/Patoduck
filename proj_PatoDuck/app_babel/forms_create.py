from django.forms import ModelForm
from django import forms
from .models import *

class CharCreateForm(ModelForm):
    class Meta:
        model = Character
        fields = '__all__'

        # ? text area field variable
        col = 2
        row = 1

        widgets = {
            'name' : forms.Textarea(attrs={
                    'rows' : row,
                    'cols' : col
                        }            
                    ),
            'name_pt' : forms.Textarea(attrs={
                    'rows' : row,
                    'cols' : col
                        }            
                    ),
            'name_es' : forms.Textarea(attrs={
                    'rows' : row,
                    'cols' : col
                        }            
                    )
            }