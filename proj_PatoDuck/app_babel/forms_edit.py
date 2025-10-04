from django.forms import ModelForm
from django import forms
from .models import *

class CharacterEditForm(ModelForm):
    class Meta:
        model = Character
        fields = "__all__"
        
class ActionEditForm(ModelForm):
    class Meta:
        model = Action
        fields = "__all__"
        
class LocationEditForm(ModelForm):
    class Meta:
        model = Location
        fields = "__all__"

class QuestEditForm(ModelForm):
    class Meta:
        model = Quest
        fields = "__all__"
        exclude = [
            "number_of_steps"
        ]
    # TODO: You might want to make a link for the conversations later
    

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


class SpeechEditForm(ModelForm):
    #? It is just not worth to edit the conversation. If you need that, go on admin
    class Meta:
        model = Speech
        
        fields = [
            'txt_en',
            'txt_pt',
            'txt_es',
            
            'name',
            'previous_speech',
            'next_speech'
        ]
        
        widgets={
                'txt_en': forms.Textarea(attrs={
                'class': 'form-field',
                'cols': 2,
                'rows': 2, 
            }),
                'txt_pt': forms.Textarea(attrs={
                'class': 'form-field',
                'cols': 2,
                'rows': 2, 
            }),
                'txt_es': forms.Textarea(attrs={
                'class': 'form-field',
                'cols': 2,
                'rows': 2, 
            }),
                # 'previous_speech': forms.ModelChoiceField(
                #     queryset=Speech.objects.filter()
                # )
        }
        
        