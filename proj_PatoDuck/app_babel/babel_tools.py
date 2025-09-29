from .models import *
from django.shortcuts import render, redirect, get_object_or_404
import pprint


def msg(txt,title="ERROR"):
    """Creates space so it doesn't get messed up among the 32 django error lines
    """
    pprint.pprint(f"""
           --------------------------------
                        [[ERROR]]
           
           
                {txt}
           
           --------------------------------
           """)

def conv_create_name(conv):
    ... # basically if conv has a quest, so on.

# TODO: Test this on the new code

def speech_create_name(conv,reply_to=None): # create names for speeches
    if conv.is_linear:
        name = f"{conv.title} [{len(Speech.objects.filter(conversation=conv.id))}]"
    elif reply_to is not None:
        num = len(Speech.objects.filter(previous_speech=reply_to))
        num += 1
        name = f"F-{reply_to.name} [{num}]"
    return name

# --------------------------------------------------------------------

def has_first_speech(conv_pk,return_speech=False):
    
    try:
        if (first_speech := Speech.objects.filter(conversation=conv_pk, is_first=True)):
            if return_speech:
                return first_speech
            else:
                return True
            
    except Speech.MultipleObjectsReturned:
        
        
        msg("has_first_speech: Multiple Firsts, marking the conversation as broken")
        
        pprint(first_speech)
        
        conv = get_object_or_404(Conversation,id=conv_pk)
        conv.broken_chain = True
        conv.save()
        
        return None #? because there is no true first, it is better to throw a wrench
        
    except Speech.DoesNotExist: #no results with first speech
        return False


                       
    
    
    
    
    
    
    
    
                

# ! maybe remove this
def tree_of_speeches(conv_pk,orphans=False):
    """
    Iterates a query and packages the hierarchy trees
    Then it will query orphans, if set to do it
    """
    ...
    