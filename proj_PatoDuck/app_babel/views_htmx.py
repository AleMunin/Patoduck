from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# my own libraries
from .models import * # ? From the project
from .forms_create import *
from .forms_edit import *
from .validations import *
from .babel_tools import *


#? Munin from the future. I know views can give a form and handle it.abs
#? Please resist the urge to do so
#? You don't need a cluttered spaghetti, you do not know
#! What kind of validations you'll need
#? And when you find out, you'll eventually mess up how the forms are sent
#? And you'll triple the time trying to test something simple

def htmx(fn_name):
    fn_intro(fn_name, "htmx")


def htmx_get_new_speech_form(request,conv_pk):
    #TODO: Add htmx request for this function(see create_speech.html)
    htmx("htmx_get_new_speech_form")
    conv = get_object_or_404(Conversation,id=conv_pk)
    
    initial_values = {
            'conversation' : conv,
            #? previous_speech can be set here, if you want
            #TODO: Pass form as instance after your tests
            #'line_hash' : create_hash(), # ! Just do a better job here with a randomizer when the form is valid.
            #TODO: 'name' : create_name(conv),
            'txt_en' : "LOLOLOL",
            'name' : "Test Name"
        }
    
    form = SpeechCreateForm(initial=initial_values)
    
    context = {
        "form" : form,
        "conv_pk" : conv_pk
    }
    return render(request,'site/forms/speech/create_speech.html', context)

def htmx_get_new_reply_form(request,reply_to_pk):
    htmx("htmx_get_new_reply_form")
    
    reply_to = get_object_or_404(Speech,id=reply_to_pk)
    
    initial_values = {
            'conversation' : reply_to.conversation,
            'previous_speech' : reply_to,
            'txt_en' : "LOLOLOL",
            'name' : "Reply Test Name"
            #'line_hash' : create_hash(), # ! Just do a better job here with a randomizer when the form is valid.
            #TODO: 'name' : create_name(conv),
        }
    
    form = ReplyCreateForm(initial=initial_values)
    
    context = {
        "form" : form,
        "reply_to_pk" : reply_to.id
    }
    return render(request,'site/forms/speech/create_reply.html', context)


def htmx_get_edit_speech_form(request,speech_pk):
    
    print("HTMX Request")
    speech = get_object_or_404(Speech, id=speech_pk)
    
    sisters = Speech.objects.filter(id=speech.conversation)
    
    initials={
        'previous_speech' : sisters
    }
    
    form = SpeechEditForm(instance=speech, initial=initials)
    
    context = {
        'form' : form,
        'speech_pk' : speech_pk
    }
    
    return render(request,'site/forms/speech/edit_speech.html', context)

