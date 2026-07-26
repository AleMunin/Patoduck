
import pprint
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse

# my own libraries
from .fioyarn import *
from .models import * # ? From the project
# from .forms_create import *
# from .forms_edit import *
from .validations import *
from .babel_tools import *

#! You can remove this
def conv_dump(conv):
    #? This is being done manually because it is easier to test and comment
    #! Just try to be fancy and clever after you know things are working
    data = [] #? this has to parry the dump for json
    
    
    #? File information ------------
    
    #data['id'] = conv.id #! might not need this
    print("\n\n\n")
    
    #pprint.pprint(data)
    data['title'] = conv.title #? Used for file names
    data['description'] = conv.description #? Context for the file
    data['condition'] = conv.condition #? Extra context if needed
    
    # data['is_quest'] = conv.is_quest #! Might not be neeeded, but keeping parity with json for now
    #             #? This should have been processed before making the files, but who knows, might need on a comment
    # data['is_cutscene'] = conv.is_cutscene
    # data['my_code'] = conv.my_code
    
    # data["is_linear"] = conv.is_linear #! Probably don't need this
    # data["quest_step"] = conv.quest_step #? naming stuff
    
    # return data
    
    
    # Uneeded: in_game
    
    

def db_to_yarn():
    
    #TODO: It might be best to start a loop through quests first
    #TODO: Then without quests
    #TODO: Then single speeches
    
    
    #for conv in Conversation.objects.all(): #! When you implement a deleted flag, add a filter here
    if (conv := Conversation.objects.filter(id="6e0ca92b-df9a-4a00-addb-358e59381e81")):
        #todo: exclude broken chain too
        
        story = Story(conv)
        
        dialogue_list = []
        
        for speech in Speech.objects.filter(conversation=conv.first()):
            dialogue_list.append( Dialogue(speech) )
        
        for dialogue in dialogue_list:
            story.collect(dialogue)
            
        story.spin_it()
        #break #! just so i get a single conv