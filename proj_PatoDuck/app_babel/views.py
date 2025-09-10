from django.shortcuts import render, redirect

# my own libraries
from .models import * # ? From the project
from .forms_create import *

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
    all_conv = Conversation.objects.values_list('title', 'id', 'is_quest', 'quest_step')
    
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

