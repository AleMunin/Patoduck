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
        
class ConditionalCreateForm(ModelForm):
    class Meta:
        model = Conditional
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
        
        # fieldsets = (
            
        # )# fieldset ends


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
               # 'readonly': 'readonly', #somehow not working, leave it commented
                'class' : 'hidden'
                #? Instead of hidden you can filter it on the __init__ to only the conv
            })
                
            
            
        }
    #! DO NOT UNCOMMENT THIS unless:
    #? You start dealing with prev/next speech
    #? I am keeping this here so you don't need to go hunt on other forms if you do
        
    #
    # def __init__(self, *args, **kwargs): #? filter the speeches to the same conversation
    #     # I hate doign this but it needs to be done on runtime, not on the models.py =/        
    #     speech = kwargs['instance']
    #     conv = speech.conversation
    #     super().__init__(*args, **kwargs)    # Here I pretend to understand the initialization of form
        
    #     if (speeches := Speech.objects.filter(conversation=conv).exclude(id=speech.id)):
    #                     #? don't try to be clever and just exclude "speech", it won't work
    #         #todo: filter deleted ones too
    #         self.fields['previous_speech'].queryset = speeches #this is the select form
    #         self.fields['next_speech'].queryset = speeches
                
   
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
            "previous_speech", #! Obligatory
            
            "fq_en",
            "fq_pt",
            "fq_es",
            
        ]
        
        
        fieldsets = (
            ("Main:", {
                'fields' : ('txt_en','txt_pt','txt_es'),
                'classes' : ('main-field'),
                'description' : "The Speech actually said",
                }
            ),
            ("Fork Question:", {
                'fields' : ('fq_en','fq_pt','fq_es'),
                'classes' : ('fork-questions'),
                'description' : "What option leads to it",
                }
            ),
            
            ("Dialogue Data:", {
                'fields' : ('previous_speech','next_speech','conversation'),
                'classes' : ('order-selection hidden'),
                'description' : "Where it is in relation ot other speeches",
                }
            ),
                
        )# fieldset ends

        
        
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
            }),
            
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
            
            
        } #widget ends
