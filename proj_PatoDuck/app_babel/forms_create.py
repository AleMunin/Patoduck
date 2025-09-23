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
        
class QuestCreateForm(ModelForm):
    class Meta:
        model = Quest
        fields = '__all__'
        
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
        fields = [ #! DO NOT ADD FORK QUESTIONS HERE FOR NOW
            # Wrapp on div "form-speech-status"
            'has_fork',
            'speaker',
            'portrait',
            
            # Wrap on div "form-speech-textbox"
            # rows 5, col 4
            'txt_en',
            'txt_pt',
            'txt_es',
            
            # ? Optional, easier to hide
            # wrap on div "form-fork-question"
            # rows 2, col 4
            # wrap on div "form-localized"
            'localized_pt',
            'localized_es',
            
            # wrap on div "optional"
            'comment',
            'my_code',
            
             # ? This will be filled by the view
             
             #wrap on div "hide form-metadata"
             # TODO: Make this read only on widgets
            'conversation',
            'previous_speech',
            'is_fork', #? maybe, idk yet
        ]
        widgets = { #? do not put disableds/readonlys here, make it more explicit so you don't end up miserable next refactor
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
            
        }
        
        #! Disables
        
        
        
        
        