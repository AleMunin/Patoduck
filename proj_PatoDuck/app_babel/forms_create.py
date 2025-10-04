from django.forms import ModelForm
from django import forms
from .models import *

#TODO:
# 1 - readonly fields don't work and disabled fields break form validation
# 2 - I did hide the forms that just carry data, but did not hide the labels
# 

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
        
class QuestCreateForm(ModelForm):
    class Meta:
        model = Quest
        fields = '__all__'
        exclude = ['number_of_steps']
        
class LocationCreateForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'
        
class ConversationCreateForm(ModelForm):
    
    
    class Meta:
        model = Conversation
        exclude = [
            "is_linear",
            "broken_chain",
            "in_game", # ? save that for editing
            "quest_step", # ? should be automated on creation
        ]
        
        col = 5
        
        widgets = {
        'location': forms.Select(attrs={
            'class': 'form-field form-dropdown',
            'data-group' : 'form-fields-dropdown'
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
        
class SpeechCreateForm(ModelForm):
    class Meta:
        model = Speech
        #fields = '__all__'
        
        fields = [
            "name",
            "txt_en",
            "txt_pt",
            "txt_es",
            "conversation"
        ]
        
        # exclude = [
        #     'is_first',
        #     'previous_speech',
        # ]
        widgets = {
            'txt_en' : forms.Textarea(attrs={
                'class': 'form-field',
                'cols': 2,
                'rows': 2, 
            }),
            
            'txt_pt' : forms.Textarea(attrs={
                'class': 'form-field',
                'cols': 2,
                'rows': 2, 
            }),
            
            'txt_es' : forms.Textarea(attrs={
                'class': 'form-field',
                'cols': 2,
                'rows': 2,
            }),
                
            'conversation' : forms.Select(attrs={
               # 'readonly': 'readonly',
                'class' : 'hidden'
            })
                
            
            
        }
                
   
class ReplyCreateForm(ModelForm):
    
    #? for now this is a different form in case i need to make modifications to it
    
    
    class Meta:
        model = Speech
        #fields = '__all__'
        
        fields = [
            "name",
            "txt_en",
            "txt_pt",
            "txt_es",
            "conversation",
            "previous_speech",
        ]
        
        widgets = {
            'txt_en' : forms.Textarea(attrs={
                'class': 'form-field',
                'cols': 2,
                'rows': 2, 
            }),
            
            'txt_pt' : forms.Textarea(attrs={
                'class': 'form-field',
                'cols': 2,
                'rows': 2, 
            }),
            
            'txt_es' : forms.Textarea(attrs={
                'class': 'form-field',
                'cols': 2,
                'rows': 2,
            }),
            
            'conversation' : forms.Select(attrs={
               # 'readonly': 'readonly',
                'class' : 'hidden'
            }),
            
            'previous_speech' : forms.Select(attrs={
               # 'readonly': 'readonly',
                'class' : 'hidden'
            })
        }
     