import pprint
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
    
class ConditionalEditForm(ModelForm):
    class Meta:
        model = Conditional
        fields = '__all__'
        exclude = ['conversation']

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
            'next_speech',
            
            
            #todo: do a check to hide those on the template
            "fq_en",
            "fq_pt",
            "fq_es",
            
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
               
               
            #! No god damn idea why col and row aren't respected 
                
            #'fn_en': forms.Textarea(attrs={
            #    'class': 'form-fork_question-field',
            #    'cols': 2,
            #    'rows': 2, 
            #}),
            
            'fq_en' : forms.Select(attrs={
                'cols': 2,
                'rows': 1, 
            }),
            
            'fq_pt' : forms.Select(attrs={
                'cols': 2,
                'rows': 1, 
            }),
            
            'fq_es' : forms.Select(attrs={
                'cols': 2,
                'rows': 1, 
            }),
            
                # 'previous_speech': forms.ModelChoiceField(
                #     queryset=Speech.objects.filter()
                # )
        }
        
    def __init__(self, *args, **kwargs): #? filter the speeches to the same conversation
        # I hate doign this but it needs to be done on runtime, not on the models.py =/        
        speech = kwargs['instance']
        conv = speech.conversation
        super().__init__(*args, **kwargs)    # Here I pretend to understand the initialization of form
        
        if (speeches := Speech.objects.filter(conversation=conv).exclude(id=speech.id)):
                        #? don't try to be clever and just exclude "speech", it won't work
            #todo: filter deleted ones too
            self.fields['previous_speech'].queryset = speeches #this is the select form
            self.fields['next_speech'].queryset = speeches
