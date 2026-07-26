import pprint
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse

# my own libraries
from .models import * # ? From the project
from .forms_create import *
from .forms_edit import *
from .validations import *
from .babel_tools import *
from .downloads import *
from .fioyarn import *

def home_view(request):
    """
    The home view is a simple count query of the database.
    The HTMX requests on buttons ARE NOT processed here.
    """

    # * General Query count
    chars = Character.objects.all()
    quests = Quest.objects.all()
    locs = Location.objects.all()
    convs = Conversation.objects.all()
    speeches = Speech.objects.all()


    context ={
        # * Page Data
        
        "view_name" : "Home",
        
        # * General Query count
        
        "all_chars" : len(chars),
        'all_locs' : len(locs),
        "all_quests": len(quests),
        "all_convs" : len(convs),
        "all_speeches" : len(speeches)
    }


    # ----------- TESTING
    
    #db_to_yarn()
    
    
    #----------------

    return render(request,'site/home.html', context )

# ? OVERVIEW ----------------------------------------------------------

def all_char_view(request):

    all_char = Character.objects.all()
    total_char= len(all_char)
    
    context ={
        
        # * Page data
        "view_name" : "All Characters",
        
        # * Character info
        "chars" : all_char, # necessary for listing
        "total_char" : len(all_char), # just to make my life easier
    }
    
    return render(request, 'site/overviews/all_char.html', context )


def all_location_view(request):
    # TODO: check if locations are part of a quest? idk
    all_loc = Location.objects.all()
    
    context = {
        
        # * Page data
        "view_name" : "All Locations",
            
        "all_loc" : all_loc,
        "total_loc" : len(all_loc)
    }
    return render(request, 'site/overviews/all_loc.html', context )

def all_quest_view(request):
    # TODO: Maybe list the number of characters in the quest, and steps?
    all_quests = Quest.objects.all()
    
    context={
        
        # * Page data
        "view_name" : "All Quests",
        
        "quests" : all_quests,
        "total_quest" : len (all_quests)
        }

    return render(request, 'site/overviews/all_quest.html', context )

def all_conv_view(request):
    # TODO: Maybe list the number of characters in the conversation.
    # all_conv = Conversation.objects.values_list('title', 'id', 'is_quest', 'quest_step')
    all_conv = Conversation.objects.all()
    context= {
        # * Page data
        "view_name" : "All Conversations",
        
        "all_conv" : all_conv,
        "total_conv" : len(all_conv)
        }
    
    return render(request, 'site/overviews/all_conv.html', context )

# ? CREATION VIEWS ----------------------------------------------------

def character_create_view(request): #creates form or save form for Character
    form = CharCreateForm()

    if request.method == 'POST':
        form = CharCreateForm(request.POST)
        if form.is_valid():
            # TODO: Check if the name didn't repeat in any language first.
            form.save()
            return redirect('all_char') # TODO: Redirect may be overkill if using modal

    return render(request,'site/forms/char/create_char.html', {'form' : form })

def quest_create_view(request): #creates form or save form for Quest
    form = QuestCreateForm()

    if request.method == 'POST':
        form = QuestCreateForm(request.POST)
        if form.is_valid():
            # TODO: Check if there are no names like that before.
            form.save()
            return redirect('all_quest')
    context = {'form' : form }

    return render(request,'site/forms/quest/create_quest.html', context)


def location_create_view(request): #creates form or save form for Location

    if request.method == 'POST':
        form = LocationCreateForm(request.POST)
        if form.is_valid():
            #TODO: validate by checking if the names aren't the same
            form.save()
            
    form = LocationCreateForm()
    
    context = {
        "form" : form
    }
    return render(request, 'site/forms/location/create_location.html', context)

def conversation_create_view(request):

    # TODO: Name for conv
    if request.method == 'POST':        # if it is processing the form with a new conversation
        form = ConversationCreateForm(request.POST)
        if form.is_valid():
            new_form = form.save()
            request.session['conv_request'] = str(new_form.id)   # get the primary key of the new conversation
            # TODO: use the new id to redirect to the conversation page
            # TODO: go to forms and make them smaller on attr
            # TODO: do not add quest step on form, make it add to the end.abs
            # TODO: Make an in-between form on the edit_conv
            # TODO: make is linear and broken chain not show up on the form
            return redirect("all_conv") # change to edit_conv.
            #redirect to a speech edit with the get method for x talk
    else:
        initials={
            "title" : "!Auto!"
        }
        form = ConversationCreateForm(initial=initials)

    return render(request,'site/forms/conversation/create_conversation.html', {'form' : form })


def cond_create_view(request,conv_pk):
    fname = "\n \033[33m cond_create_view \033[0m"
    fn_intro(f"cond_create_view")
    
    if request.method == 'POST':
        form = ConditionalCreateForm(request.POST)
        if form.is_valid():
            
            #todo: Validate cond?
            print(f"{fname}: Form was valid")
            
            cond = form.save()
            context = {'cond' : cond }
            return render(request,'site/read/single/single_cond.html', context)


def speech_create_view(request,conv_pk):
    
    fname = "\n \033[33m speech_create_view \033[0m"
    fn_intro(f"speech_create_view")
    #conv = get_object_or_404(Conversation,id=conv_pk)
        
    if request.method == 'POST':
        form = SpeechCreateForm(request.POST)
        
        if form.is_valid():
            print(f"{fname}: Form was valid")
            speech = validate_reply(form.save(commit=False))          
            context = {
                'speech' : speech
            }
            
            print(f"{fname}: Will now render back the single speech")
            #return HttpResponse("This was a triumph")
            return render(request,'site/read/single/single_speech.html', context)

        else:
            msg("Speech Form was invalid")
            return HttpResponse(form_errors(form.errors.items()))
    else:
        msg("speech_create_view did receive a non-POST request")


def reply_create_view(request,reply_to_pk):
    
    fname = "\n \033[33m reply_create_view \033[0m"
    fn_intro(f"reply_create_view")
    
    previous = get_object_or_404(Speech,id=reply_to_pk)
        
    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        
        if form.is_valid():
            print(f"{fname}: Form was valid")
            
            reply = form.save(commit=False)
            reply.previous_speech=previous #? always before validation
            reply = validate_reply(reply)
            
            context = {
                'speech' : reply
            }
            
            print(f"{fname}: Will now render speech")
            
            #return HttpResponse("This was a triumph") #todo: change to render it on page
            return render(request,'site/read/single/single_speech.html', context)
        else:
            msg("Reply Speech Form was invalid")
            return HttpResponse(form_errors(form.errors.items())) #todo maybe format this into a function
    else:
        msg("speech_create_view did receive a non-POST request")

            
# ? Edit Profiles

def edit_char_view(request,pk):
    char = get_object_or_404(Character, id=pk)

    if request.method == 'POST':
        form = CharacterEditForm(request.POST, instance=char)
        if form.is_valid():
            print("\n\n FORM WAS VALID!")
            form.save()
            return redirect('all_char')
        else:
            msg("Form was invalid")
    
    form = CharacterEditForm(instance=char)

    return render(request,'site/forms/char/edit_char.html', {'form' : form })


def edit_quest_view(request,pk):
    quest = get_object_or_404(Quest, id=pk)

    if request.method == 'POST':
        form = QuestEditForm(request.POST, instance=quest)
        if form.is_valid():
            print("\n\n\ FORM WAS VALID!")
            form.save()
            return redirect('all_quest')
        else:
            msg("Form was invalid")
    
    form = QuestEditForm(instance=quest)

    return render(request,'site/forms/quest/edit_quest.html', {'form' : form })


def edit_cond_view(request,cond_pk):
    cond = get_object_or_404(Quest, id=cond_pk)

    if request.method == 'POST':
        form = ConditionalEditForm(request.POST, instance=cond)
        if form.is_valid():
            cond =  form.save()
            return render(request,'site/single/single_cond.html', {'cond' : cond })



def edit_loc_view(request,pk):
    loc = get_object_or_404(Location, id=pk)

    if request.method == 'POST':
        form = LocationEditForm(request.POST, instance=loc)
        if form.is_valid():
            form.save()
            return redirect('all_location')
    
    form = LocationEditForm(instance=loc)

    return render(request,'site/forms/location/edit_location.html', {'form' : form })


def edit_conv_view(request,pk):    
    """
    Called either by edit button or directly from creation of a conv.
    !   It will create forms to be rendered for speeches, but it WILL NOT receive them. That is for htmx modal views
    
    """
    
    def add_forks(speech):
        
        all_forks = [speech]
        forks = Speech.objects.filter(previous_speech=speech.id)

        for fork in forks:
            all_forks.append( add_forks(fork) )  
            
        print(f"my print is {speech.name}")
        print("the results are:")
        pprint.pprint(all_forks)
        return all_forks
    
    conv = Conversation.objects.get(id=pk) #todo: maybe put get or 404 

    # POST HANDLING --------------------------------

    if request.method == 'POST':
        new_conv = ConversationEditForm(request.POST, instance=conv)
        if new_conv.is_valid():
            # TODO: Conv validation
            new_conv.save()
            conv_form = ConversationEditForm(instance=Conversation.objects.get(id=pk))
            #? this was queried again because using the new_conv, though saved, would cause errors.
        else:
            conv_form = new_conv
            # ! I couldn't test that ✖‿✖
            
    else: #? If not post
        conv_form = ConversationEditForm(instance=conv)
        
    # Speech list handling -------------------------
        #? This could probably replace the tree_of_speeches code
    
    if (first_speech := has_first_speech (pk,True)):
        all_speeches = add_forks(first_speech.first())
    else:
        all_speeches = []
    # Context ------------------------------------------
    context = {
        'pk' : pk,  #no need to be this way but i'm fed up
        'conv_form' : conv_form,
        'conv' : conv, # ? it will print the original conv there
        # TODO: 'speech_form' : speech_form, actually this can be asked on htmx
        'speeches' : all_speeches

    }
    
    print("\n\n\n\n\n")
    pprint.pprint(all_speeches)
    
    return render(request,'site/forms/conversation/edit_conv.html', context)

def edit_speech_view(request,speech_pk):
    #? This does not return forms, check htmx views
    
    print("\n\n edit_speech request: \n\n")
    
    speech = get_object_or_404(Speech,id=speech_pk)
    
    if request.method == 'POST':
        form = SpeechEditForm(request.POST, instance=speech)
        
        
        if form.is_valid():
            edited_speech = form.save(commit=False)
            if validate_reply(edited_speech):
                
                print("\n\n\n\n\n\n Okay so far \n\n\n\n")
                return render(request,'site/read/single/single_speech.html', { 'speech' : speech } )
            
            # replace the form rendering the speech again
            
