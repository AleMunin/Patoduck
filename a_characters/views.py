from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import *
from .forms import *
from .tools import *
from .downloads import *

from django import forms 
from django.forms import ModelForm  # because apparently importing forms or * was not working.

from django.http import JsonResponse, HttpResponse

# TODO: Fork Form & processing, Cycle-Back protocol, Edit, Deletion, Splitting, User Autorization


# ? Comentários tem cor
# Comentário normal
# TODO: 
# * Comentário
# ! Comentário

# Create your views here.

# RUles of Thumb:

# "process" functions can be registered as views, but are usually just HTMX responses
# functions not called views or processes are usually called by others


# FULL PAGE VIEWS ====================================================================

def home_view(request):
    """
    The home view is a simple count query of the database.
    The HTMX requests on buttons are not processed here.
    """

    chars = Character.objects.all()
    quests = Quest.objects.all()
    locs = Location.objects.all()
    convs = Conversation.objects.all()
    speeches = Speech.objects.all()


    context ={
        "all_chars" : len(chars),
        'all_locs' : len(locs),
        "all_quests": len(quests),
        "all_convs" : len(convs),
        "all_speeches" : len(speeches)
    }

    return render(request,'site/home.html', context )


# Menu

def menu(request):
    # ! This is not using any kind of authentication
    
    ...

# PAGE LISTERS ====================================================================

def all_char_view(request):

    all_char = Character.objects.all()
    total_char= len(all_char)
    return render(request, 'site/all_char.html', { "chars" : all_char, "total_char" : total_char } )

def all_location_view(request):
    # TODO: check if locations are part of a quest? idk
    all_loc = Location.objects.all()
    total_loc= len(all_loc)

    context = {
        "all_loc" : all_loc,
        "total_loc" : total_loc
    }
    return render(request, 'site/all_loc.html', context )

def all_quest_view(request):
    # TODO: Maybe list the number of characters in the quest, and steps?
    all_quests = Quest.objects.all()
    total_quest = len(all_quests)

    return render(request, 'site/all_quests.html', { "quests" : all_quests, "total_quest" : total_quest } )

def all_conv_view(request):
    # TODO: Maybe list the number of characters in the conversation.
    all_conv = Conversation.objects.values_list('title', 'id', 'is_quest', 'quest_step')
    total_convs = len(all_conv)
    
    return render(request, 'site/all_conv.html', { "convs" : all_conv, "total_conv" : total_convs } )


# CRUD Views ====================================================================

# Character ----------------------------------------------------

def character_create_view(request): #creates form or save form for Character
    form = CharCreateForm()

    if request.method == 'POST':
        form = CharCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request,'site/forms/char/create_char.html', {'form' : form })

# Location ----------------------------------------------------

def location_create_view(request): #creates form or save form for Location

    if request.method == 'POST':
        form = LocationCreateForm(request.POST)
        if form.is_valid():
            form.save()
            
    form = LocationCreateForm()
    
    context = {
        "form" : form
    }
    return render(request, 'site/forms/loc/create_location.html', context)

    
# Quest -----------------------------------------------------

def quest_create_view(request): #creates form or save form for Quest
    form = QuestCreateForm()

    if request.method == 'POST':
        form = QuestCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request,'site/forms/create_quest.html', {'form' : form })

# Conversation -----------------------------------------------------

def conversation_create_view(request):
    #form = ConversationCreateForm()

    if request.method == 'POST':        # if it is processing the form with a new conversation
        form = ConversationCreateForm(request.POST)
        if form.is_valid():
            new_form = form.save()
            request.session['conv_request'] = str(new_form.id)   # get the primary key of the new conversation

            return redirect("all_conv") # change to edit_conv.
            #redirect to a speech edit with the get method for x talk
    else:
        form = ConversationCreateForm()

    return render(request,'site/forms/create_conversation.html', {'form' : form })


def edit_conv_view(request,pk):
    print("")
    
    conv = Conversation.objects.get(id=pk)
    #conv_name = f"{conv.title} Speech []"
    conv_name = create_name(conv)

    conv_form = ConversationEditForm(instance=conv)


    initial_values = {
        'conversation' : pk,
        'name' : conv_name,
        'txt_en' : "LOLOLOL" }

    speech_form = SpeechCreateForm(initial=initial_values)

    # This section will be updated with the HTMX stuff.
    # Maybe we leave this function to only get this.

    if request.method == 'POST':
        #remove instance, add initial? Careful with name order
        new_conv = ConversationEditForm(request.POST, instance=conv)
        if new_conv.is_valid():
            new_conv.save()

            conv_form = new_conv
            conv = Conversation.objects.get(id=pk)
            #you can also add old_conv to show a com a comparison

    # Get all speeches linked to this
    speeches = Speech.objects.filter(conversation=pk)


    context = {

        'pk' : pk,  #no need to be this way but i'm fed up
        
        'conv_form' : conv_form,
        'conv' : conv,
        #'old_conv' : old_conv

        'speech_form' : speech_form,

        'speeches' : speeches

    }
    return render(request,'site/forms/edit_conv.html', context)

# Speeches -----------------------------------------------------

def get_new_speech(request,conv_pk):    # Handles LINEAR conversation speeches form

    conv = get_object_or_404(Conversation,id=conv_pk)

    if request.method == 'POST':
        if conv.is_linear:
            initial_values = {
                'conversation' : conv_pk,
                'line_hash' : create_hash(), # ! Just do a better job here with a randomizer when the form is valid.
                'name' : create_name(conv),
                'txt_en' : "LOLOLOL"
            }

            form = SpeechLinearCreateForm(initial=initial_values) #SpeechCreateForm(initial=initial_values) can test with

            context = {
                'pk' : conv_pk,
                'speech_form' : form
            }

            return render(request, 'site/forms/create_speech.html', context)
        
        else:
            print(" !!!!! Conversation isn't linear anymore. You shouldn't be able to make this request")
    else:
        print(f"    !!!!! Non POST request asked for get_new_speech")

def create_speech_process(request,pk,dbug=False): # saves speech, returns saved speech or None
    conv = get_object_or_404(Conversation,id=pk)

    is_fork = False
    speech = None

    if request.method == 'POST':
        form = SpeechLinearCreateForm(request.POST)


        if form.is_valid():
            form.conversation = conv
            speech =form.save(commit=False)
    
            validation = validate_new_speech(speech,conv) # This is wrong, should return false
            if validation[0]:
                
                speech = validation[1]

                speech.save()
            
                return render(  #returns for the htmx
                    request,'site/htmx/single_speech.html',
                    {'speech' : speech, 'is_fork' : is_fork }) # will be replaced with render
            else:
                #print speech_status?
                #return HttpResponse(f"Well, {speech.name} was not valid.")
                print("Something went wrong with validation of the speech")
                return render(request,'site/htmx/errors/invalid_speech.html',{})

        else:
            print("")
            print("Form was not valid")
            pprint(f"Following errors\n {form.errors}")
            return render(request,'site/htmx/errors/invalid_speech.html',{})
        
    else:
        return HttpResponse("What were you thinking? This is not a post")
        


def create_fork_view(request,reply_pk,fork_letter,conv_pk): # Gets form 
    reply_to = get_object_or_404(Speech,id=reply_pk)
    conv = get_object_or_404(Conversation,id=conv_pk)

    if request.method == 'POST':
        form = SpeechCreateForm(request.POST)
        if form.is_valid():
            speech =form.save(commit=False)
            
            speech = validate_speech(speech,conv)
        return render(  #returns for the htmx
            request,'site/htmx/single_speech.html',
            {'speech' : speech, 'is_fork' : is_fork }) # will be replaced with render

    else:
        initial_values = {
            "previous_speech" : reply_to.id, #if this fails just use full object
            "is_fork" : True,
            "fork_letter" : fork_letter,
            }

        form = SpeechCreateForm(initials=initial_values)
        
        # return the form for create speech



# all conv view
# queries ONLY non-fork ones.
# if has_fork, loops on that to put the loops on the list[], directly after the "parent"

# fork_create_view

# FORK QUESTION HANDLING INSIDE SPEECH -----------------------------------------------------

def fork_question_process(request,speech_pk): # Processes the Fork Question FORM

    # ! This function was being tested, don't implement the wrap before you re-test

    def wrap_html(fields):
        """
        <!-- ------------------ FORK (letter) --------------------------  -->
        <div class = "fork_wrapper wrapper> Non negotiable
            <fieldset class= "field_en">
                <h6> Fork (letter) </h6>
                <label>(Language) </label>

                {{ form.fork_queston_en_A}}
            </fieldset>

        </div>
        """

    speech = get_object_or_404(Speech,id=speech_pk)
    conv = get_object_or_404(Conversation,id=speech.conversation)

    if request.method == 'POST':
        form = ForkCreateForm(request.POST, instance=speech)

        if form.is_valid():
            form.save()
            speech.has_fork=True
            speech.save()
            conv.is_linear = False
            conv.save()

            msg = "The fork worked" # delete this out of context
            
            return render(request,'site/htmx/fork_speech_form.html', { 'speech' : speech, 'msg' : msg }) 
        else:
            print("the form is NOOOOOOOOOOOOOOOOOOOOOOT VALID \n\n\n")

def get_fork_question(request,speech_pk): # Returns the FORM for Fork Question.
    # gets speech form where speech_pk is the one being replied to
    # This form is merely to use the fork fields.
    # The render once it is accepted immediately calls a branch_speech_process fork

    speech = get_object_or_404(Speech,id=speech_pk)
    

    if request.method == 'POST':

        my_initials = get_fork_fields(speech,"all")

        form = ForkCreateForm(instance=speech, initial=my_initials)

        # Preparing form fields data for template -------------------------------

        # I am very aware i could make lists inside lists, but i HATE the template
        # of django when it comes to loops so that is how it is going to bef or today

        en_forks= get_fork_fields(speech,'en')
        pt_forks= get_fork_fields(speech,'pt')
        es_forks= get_fork_fields(speech,'es')

        # en_empties=[] # template's for each loop will check if it will hide the field or not
        # pt_empties=[]
        # es_empties=[]
        # field_groups = [] # False is all fields are empty

        # en_all_false = True

        # for en, pt, es in zip(en_forks, pt_forks, es_forks):
        #     en_empties.append(True) if en is None else en_empties.append(False)
        #     pt_empties.append(True) if pt is None else pt_empties.append(False)
        #     es_empties.append(True) if es is None else es_empties.append(False)


        #     if (en is None) and (pt is None) and (es is None):
        #         field_groups.append(False) # false
        #     else:
        #         field_groups.append(True) # field is in use

        
        context = {
            'form' : form,

            'speech' : speech, # mostly for the speech id formation, pk was giving trouble

        }


        return render(request,'site/htmx/fork_speech_form.html', context) 


# def get_new_fork(request,speech_pk):

#     reply_to = get_object_or_404(Speech, id=speech_pk)
#     conv = get_object_or_404(Conversation, id=reply_to.conversation)

#     initial_values = [
#         "name": create_name(conv, reply_to),
#         "is_fork" : True,
#         "previous_speech" : speech_pk,
#         "line_hash" : create_hash(),

#     ]

#     # * Before you exit:
    
    
#     reply_to.has_fork = True 
#     conv.is_linear = False # This has to be re-affirmed go here otherwise it can screw up vaidation
#     reply_to.save()
#     conv.save()