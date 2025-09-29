from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# my own libraries
from .models import * # ? From the project
from .forms_create import *
from .forms_edit import *
from .validations import *
from .babel_tools import *


def htmx_get_new_speech_form(request,conv_pk):
    #TODO: Add htmx request for this function(see create_speech.html)
    conv = get_object_or_404(Conversation,id=conv_pk)
    
    initial_values = {
            'conversation' : conv,
            #? previous_speech can be set here, if you want
            
            #'line_hash' : create_hash(), # ! Just do a better job here with a randomizer when the form is valid.
            #TODO: 'name' : create_name(conv),
            'txt_en' : "LOLOLOL"
        }
    
    form = SpeechCreateForm(initial=initial_values)
    
    context = {
        "form" : form,
        "conv_pk" : conv_pk
    }
    return render(request,'site/forms/speech/create_speech.html', context)


def htmx_get_edit_speech_form(request,speech_pk):
    speech = get_object_or_404(Speech, id=speech_pk)
    return render(request,'site/forms/speech/create_speech.html', context)
    