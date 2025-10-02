from .models import *
from .validations import *

from django.shortcuts import render, redirect, get_object_or_404
import pprint

#? Yes, this code is wet
#? I am fully aware there are a lot of redundant queries
#? I want the functions to be as independent as possible
#? It won't hurt because this is a two users application
#? If I wanted speed I would be doing this in Go


def msg(txt,title="ERROR"):
    """Creates space so it doesn't get messed up among the 32 django error lines
    """
    pprint.pprint(f"""
           --------------------------------
                        [[ERROR]]
           
           
                {txt}
           
           --------------------------------
           """)

def form_errors(errors):
    #? input is form.errors.items()
    error_msg = "<p>Form is valid but Conversation is Broken</p>"
    for field, error in errors:
        errors = f"{field}: {error}"
        print(error)
        error_msg += f"<p> {error} </p>"
        
    return error_msg
                        
def obj_check():
    # check if it is is_object or a string, if a string it will query
    # make one for every object.
    
    ...


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

    ...


def has_first_speech(conv_pk,return_speech=False):
    """Checks if an object has a first speech or not
    Returns False if it doesn't have one
    Returns True if it has
    Returns Speech Object if it has one and return_speech was flagged true
    
    """
    try:
        if (first_speech := Speech.objects.filter(conversation=conv_pk, is_first=True)):
            if return_speech:
                return first_speech
            else:
                return True
            
    except Speech.MultipleObjectsReturned:
        
        
        msg("has_first_speech: Multiple Firsts, marking the conversation as broken")
        pprint(first_speech)
        
        break_conv(conv_pk)
        
        return None #? because there is no true first, it is better to throw a wrench
        
    except Speech.DoesNotExist: #no results with first speech
        return False
                       
def give_last_speech(conv_pk):
    """
    Returns 2 values
    
    First Value:
    Speech object -> if linear.
    False -> if error
    None -> if empty or forked.
    
    Second Value:
    
    True -> If it is linear (empty counts as linear)
    False -> If forked
    
    """
    #todo maybe make a check if it is a Speech object or a string
    conv = get_object_or_404(Conversation,id=conv_pk)
    
    if conv.broken_chain:
        msg("last_speech: Conversation is broken. Sort your poopoo together")
        return False#, False
    
    if conv.is_linear:
        
        try:
            if (last_speech := Speech.objects.filter(conversation=conv_pk, previous_speech=None)):
                
                print('\n\n give_last_speech: Linear speech, trying to find last') 
                pprint.pprint(last_speech)
                
                return last_speech.first()#, True
        
        except Speech.MultipleObjectsReturned:
        
            msg("last_speech: Multiple Lasts, but marked as linear marking the conversation as broken")
            break_conv(conv_pk)
            
            return None#, False
        
        except Speech.DoesNotExist:
            
            #? The speech could be fullt cycled. Which is an infinite loop in-game
            #? More importantly, it shouldn't be marked as linear
            
            if not Speech.objects.filter(conversation=conv_pk):
                
                msg("last_speech: No posts, nothing wrong except the fact this function was called", "ODD")
                
                return (None, True) #? Empty new conversations are empty
            else:
                msg("last_speech: No lasts. Possible full cycle and infinite loop. Breaking conv for good measure")
                break_conv(conv_pk)
                
                return False#, False
        
    else:
        return None#, False
        
# def linear_check(conv_pk):
#     #? just for readability
#     last, linear = give_last_speech(conv_pk)
#     return linear




def validate_reply(speech):
    """
    Validates the hierarchy, for:
        - New Speeches
        - Forks
        - Replies
        - Edits
    
    #! This function makes a lot of assumptions about
        - conversation not being broken.
        - form.is_valid() returning true
    """
    print("\n\n")
    #pprint.pprint(speech.conversation.description)
    print ("--------------------------------------")
    
    conv = speech.conversation
    
    #? Check if this is the first speech --------------------
    
    #last_speech, linear = give_last_speech(conv.id)
    last_speech = give_last_speech(conv.id)
    print ("Nachos!")
    linear = conv.is_linear # TODO: make validation there
    
    if speech.previous_speech is not None:
        parent = speech.previous_speech
    else:
        if not has_first_speech(conv.id):
            speech.is_first = True
            speech.save()
            
            return speech #? mostly just to break the function
        elif last_speech:
            
            speech.previous_speech = last_speech
            speech.save()
            
            #todo: last_speech.next_speech = speech
            last_speech.save()
            
            return speech
        else:
            # todo: maybe deal with orphans here?
            msg("validate_reply: Odd scenario, not saving speech")
            
            return False
    
    #? Check for other options ------------------------------
    
    if linear: # todo and parent.next_speech is speech: #? linear edit
        speech.save()
            
    elif linear: #todo and parent.next_speech is None: #? new speech in linear
        
        # todo: parent.next_speech = speech
        parent.save()
        speech.save()
        
    #elif (not linear and parent.next_speech is speech) or (parent.next_speech is not None): #? If harmlessly/temporarily broken
    else:  #? this more general approach should be safer
        for fork in Speech.objects.filter(previous_speech=parent): #? this could be a single id but this is safer
            fork.is_fork = True
            fork.save()
        
       # todo:  parent.next_speech = None #? if child wasn't in the loop you have bigger problems
        parent.has_fork = True
        
        speech.is_fork = True #? for good measure
        conv.is_linear = False #? same here
        
        
        conv.save()
        parent.save()
        speech.save()

    return speech
