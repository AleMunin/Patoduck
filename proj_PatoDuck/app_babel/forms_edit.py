from django.forms import ModelForm
from django import forms
from .models import *

class ConversationEditForm(ModelForm): #edits the conversation, not the speeches
    class Meta:
        model = Conversation
        fields = [
            'title',
            'quest', # TODO: validation if you unmark it, or if you mark it
            # 'quest_step', # ! If you edit this, make validation to adjust others
            'is_cutscene',
            'condition',
            'description',
            'my_code',
            'location',
        ]
        
        
        widgets = {
        'location': forms.Select(attrs={
            'class': 'form-field form-dropdown',
            'data-group' : 'form-fields-dropdown' #? testing
        }),
        'quest': forms.Select(attrs={
            'class': 'form-field form-dropdown',
            'data-group' : 'form-fields-dropdown'
        }),
        'description': forms.Textarea(attrs={
            'class': 'form-field',
            'cols': 2,
            'rows': 2, 
        }),
        'condition': forms.Textarea(attrs={
            'class': 'form-field',
            'cols': 2,
            'rows': 2, 
        }),
        'my_code': forms.Textarea(attrs={
            'class': 'form-field',
            'cols': 2,
            'rows': 2,  
        }),
    }

        