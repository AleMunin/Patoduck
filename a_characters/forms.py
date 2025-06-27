# The forms used on views are here unless they're default to a single view.

from django.forms import ModelForm
from django import forms
from .models import *


#Regular

class CharCreateForm(ModelForm):
    class Meta:
        model = Character
        fields = '__all__'

class LocationCreateForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

class QuestCreateForm(ModelForm):
    class Meta:
        model = Quest
        fields = '__all__'

class ConversationCreateForm(ModelForm):
    class Meta:
        model = Conversation
        fields = '__all__'

class ForkCreateForm(ModelForm): 
    class Meta:
            model = Speech
            fields = [
                'fork_question_en_A',
                'fork_question_pt_A',
                'fork_question_es_A',
                
                'fork_question_en_B',
                'fork_question_pt_B',
                'fork_question_es_B',

                'fork_question_en_C',
                'fork_question_pt_C',
                'fork_question_es_C',

                'fork_question_en_D',
                'fork_question_pt_D',
                'fork_question_es_D',

                'fork_question_en_E',
                'fork_question_pt_E',
                'fork_question_es_E',

                'fork_question_en_F',
                'fork_question_pt_F',
                'fork_question_es_F',
                ]


# Huge Ass stravaganza because I wanted to deal with divs.


class ConversationEditForm(ModelForm): #edits the conversation, not the speeches
    class Meta:
        model = Conversation
        fields = ['title', 'is_quest', 'quest', 'quest_step', 'is_cutscene', 'condition','description']
        labels = {
            'body' : '',
        }

    # CONDITIONALS
    def __init__(self, *args, **kwargs): # there would be probably a better way but i can't be bothered
        super(ConversationEditForm, self).__init__(*args, **kwargs) #inheritance beurocracy

        #Those will toggle when "is quest is selected"
        self.fields['is_quest'].widget.attrs.update({'id': 'is_quest_conv'})
        self.fields['quest'].widget.attrs.update({
            'id'   : 'quest_select',
            'class': 'hidden_for_now'
            })
        self.fields['quest_step'].widget.attrs.update({
            'id'   : 'quest_step',
            'class': 'hidden_for_now'
            })
        

class SpeechLinearCreateForm(ModelForm):
    class Meta:
        model = Speech
        fields = [
            'name',
            'comment',
            'my_code',
            'txt_en',
            'txt_pt',
            'txt_es',
            'conversation', #hide that field
            'line_hash',
            'speaker',
            
            
           #'localized_pt'
           # 'localized_es'
           # 'portrait',
           # 'has_fork',

        ]

class SpeechCreateForm(ModelForm):
    class Meta:
        model = Speech
        fields = '__all__' #maybe remove that because we don't want the name or conversation

    #this way I don't need to know the default field type to add class

    def __init__(self, *args, **kwargs): # there would be probably a better way but i can't be bothered
        super(SpeechCreateForm, self).__init__(*args, **kwargs) #inheritance beurocracy

        # Regular

        self.fields['name'].widget.attrs.update({'class': 'speech_name'})

        # Hidden

        self.fields['txt_es'].widget.attrs.update({'class': 'speech_name hide_annoying_parent'})

        self.fields['previous_speech'].widget.attrs.update({'class': 'speech_name hide_annoying_parent'})
        self.fields['next_speech'].widget.attrs.update({'class': 'next_speech hide_annoying_parent'})

        self.fields['fork_question_en_A'].widget.attrs.update({'class': 'fork_A hide_annoying_parent'})
        self.fields['fork_question_pt_A'].widget.attrs.update({'class': 'fork_A hide_annoying_parent'})
        self.fields['fork_question_es_A'].widget.attrs.update({'class': 'fork_A hide_annoying_parent'})

        self.fields['fork_speech_AA'].widget.attrs.update({'class': 'fork_A hide_annoying_parent'})

        self.fields['fork_question_en_B'].widget.attrs.update({'class': 'fork_B hide_annoying_parent'})
        self.fields['fork_question_pt_B'].widget.attrs.update({'class': 'fork_B hide_annoying_parent'})
        self.fields['fork_question_es_B'].widget.attrs.update({'class': 'fork_B hide_annoying_parent'})

        self.fields['fork_speech_BB'].widget.attrs.update({'class': 'fork_B hide_annoying_parent'})

        self.fields['fork_question_en_C'].widget.attrs.update({'class': 'fork_C hide_annoying_parent'})
        self.fields['fork_question_pt_C'].widget.attrs.update({'class': 'fork_C hide_annoying_parent'})
        self.fields['fork_question_es_C'].widget.attrs.update({'class': 'fork_C hide_annoying_parent'})

        self.fields['fork_speech_CC'].widget.attrs.update({'class': 'fork_C hide_annoying_parent'})

        self.fields['fork_question_en_D'].widget.attrs.update({'class': 'fork_D hide_annoying_parent'})
        self.fields['fork_question_pt_D'].widget.attrs.update({'class': 'fork_D hide_annoying_parent'})
        self.fields['fork_question_es_D'].widget.attrs.update({'class': 'fork_D hide_annoying_parent'})

        self.fields['fork_speech_DD'].widget.attrs.update({'class': 'fork_D hide_annoying_parent'})

        self.fields['fork_question_en_E'].widget.attrs.update({'class': 'fork_E hide_annoying_parent'})
        self.fields['fork_question_pt_E'].widget.attrs.update({'class': 'fork_E hide_annoying_parent'})
        self.fields['fork_question_es_E'].widget.attrs.update({'class': 'fork_E hide_annoying_parent'})

        self.fields['fork_speech_EE'].widget.attrs.update({'class': 'fork_E hide_annoying_parent'})

        self.fields['fork_question_en_F'].widget.attrs.update({'class': 'fork_F hide_annoying_parent'})
        self.fields['fork_question_pt_F'].widget.attrs.update({'class': 'fork_F hide_annoying_parent'})
        self.fields['fork_question_es_F'].widget.attrs.update({'class': 'fork_F hide_annoying_parent'})

        self.fields['fork_speech_FF'].widget.attrs.update({'class': 'fork_F hide_annoying_parent'})
                                                 
        # hide_annoying_parent and Read Only 
        # tried and didn't work, will deal with it later.
        self.fields['conversation'].widget.attrs.update({'class': 'speech_conv hide_annoying_parent'})




# HTMX Snippets