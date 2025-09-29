import pprint
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# my own libraries
from .models import * # ? From the project
from .forms_create import *
from .forms_edit import *
from .validations import *
from .babel_tools import *

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

    return render(request,'site/forms/quest/create_quest.html', {'form' : form })


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
        form = ConversationCreateForm()

    return render(request,'site/forms/conversation/create_conversation.html', {'form' : form })


def linear_create_view(request,conv_pk):
    
    conv = get_object_or_404(Conversation,id=conv_pk)
    
def fork_create_view(request,conv_pk,prev_pk):
    ...

def old_speech_create_view(request,conv_pk,reply_to=None,fork_form=False):
    
    conv = get_object_or_404(Conversation,id=conv_pk) # prevents speech to be orphan
    
    if request.method != "POST":
        form = SpeechCreateForm()
        
        # if reply_to is None:
            # query if conv has speeches, if not mark this speech form as is_first
        # if reply_to has fork, call function to find out which letter should it have
        # if reply_to has no fork, and fork_form is True, add first letter.
        # if reply_to has no fork, and fork_form is False, it will be linear
        
        
        context = {
            "form": form
        }
        
        # TODO: return render(request,'site/forms/speech/create_speech.html', {'form' : form })
    
    else:
        form = SpeechCreateForm(request.POST)
        if form.is_valid():
            
            # is it a response
            
            
            form.save()
            
# ? Edit Profiles


def add_html_forks(speech):
    # just say fuck it and print safe through here
    all_forks = [speech]
        
    forks = Speech.objects.filter(previous_speech=speech.id)

    for fork in forks:
        all_forks.append( add_forks(fork) )  
        

    return all_forks

def edit_conv_view(request,pk):    
    """
    Called either by edit button or directly from creation of a conv.
    !   It will create forms to be rendered for speeches, but it WILL NOT receive them. That is for htmx modal views
    
    """
    
    def add_forks(speech):
        
        #all_forks =[]
        #all_forks.append(speech)
        
        all_forks = [speech]
        
        forks = Speech.objects.filter(previous_speech=speech.id)

        for fork in forks:
            all_forks.append( add_forks(fork) )  
            
        print(f"my print is {speech.name}")
        print("the results are:")
        pprint.pprint(all_forks)
        return all_forks
    
    conv = Conversation.objects.get(id=pk)

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
    
    #all_speeches = []

    if (first_speech := has_first_speech (pk,True)):
        # TODO: Probably should use prefetch here, but screw it
        
        #all_speeches.append(first_speech.first())
        #all_speeches.append(add_forks(first_speech.first()))
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
    
    print("")
    print("")
    print("")
    print("")
    print("")
    pprint.pprint(all_speeches)
    
    return render(request,'site/forms/conversation/edit_conv.html', context)


def speech_create_view(request,conv_pk):
    conv = get_object_or_404(Conversation,id=conv_pk)
    
    if request.method == 'POST':
        form = SpeechCreateForm(request.POST)

        if form.is_valid():
            
            print (" FORM WAS VALID, TIME DIDN'T BITCH SO FAR")
            
            
            form.conversation = conv
            
            print(" Right before saving, let's see" )
            form.save()
            
            return HttpResponse("<h1> Saved! </h1>")
            # if not has_first_speech(conv_pk):
            #     form.is_first = True
            #     form.save()
                
            #     print("speech_create_view: First Speech Saved")
            #     return HttpResponse("Nachoooos")
                
            # else:
            #     # TODO: is_first_speech is not throwing errors right now. So careful with that
            #     if conv.is_linear:
                    
            #         try:
                        
            #            last_speech = Speech.objects.filter(conversation=conv_pk, next_speech = None)
            #            form.previous_speech = last_speech
            #            last_speech.next_speech = form.save()
            #            last_speech.save()
                       
                       
                       
            #         except Speech.DoesNotExist:
            #             conv.broken_flag = True
            #             conv.save()
                        
            #             print( " speech_create_view ERROR: Linear Conversation has no empty next speeches. Did you edit a ciruclar talk by accident?")

            #         except Speech.MultipleObjectsReturned:
            #             conv.broken_flag = True
            #             conv.save()
            #             # TODO: Make a log of them somewhere
            #             print (" speech_create_view ERROR: Two or more next_speech fields empty on a linear query. Possible fork unmarked")
            #     else:
            #         ...
            #         # TODO: Deal with forks here? Idk.
                        
            # ? Add is response to
        else:
            
            print( "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   Form invalid?")
            
            for field, errors in form.errors.items():
                print(f"{field}: {errors}")