from .models import *
from .validations import *

from django.shortcuts import render, redirect, get_object_or_404
import pprint
from string import ascii_uppercase

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
                        [[{title}]]
           
           
                {txt}
           
           --------------------------------
           """)

def fn_intro(fn_name, type="view"):
    
    end = " \033[0m "
    
    match type:
        case "view":
            start = " \033[1;32m " #green
            
        case "validation":
            start = " \033[31m " # red
            
        case "htmx":
            start = " \033[36m "  #blue

    msg = f" \n\n ------------- \n {start} {fn_name} {end} begins : \n"

    print (msg)

def form_errors(errors):
    #? input is form.errors.items()
    error_msg = "<p>Form is valid but Conversation is Broken</p>"
    for field, error in errors:
        errors = f"{field}: {error}"
        print(error)
        error_msg += f"<p> {error} </p>"
        
    return error_msg
            
def break_conv(conv):
    if type(conv) is not Conversation:
        conv = get_object_or_404(Conversation, id=conv)
    
    conv.broken_chain = True
    conv.save()
                        
def obj_check():
    # check if it is is_object or a string, if a string it will query
    # make one for every object.
    
    ...



# TODO: Test this on the new code

def speech_create_name(obj=None,model_type=None): # create names for speeches
    """
    obj = either Speech or Conversation
    model_type = "speech" or "conv"
    returns string
    #! DO NOT use primary key, pass  the object.

    """
    
    if obj:
        match model_type:
            case "speech": # Will get the name from parent
                ...
                
            case "conv":
                ...
                 # check if it is the first
                 # check if linear
                 # if not throw an error
    else:
        ... # raise error and give default name

    ...
    
def validate_conv_name(conv):
    #? This is mostly a convention enforcer for convenience rather than actual validation
    
    nameless_token = "N@meless Conv"
    questless_token = "Qüestless"
    fname = "\n \033[33m conv create name\033[0m"

    if "!Auto!" in conv.name:
        
        if conv.is_quest:
            if not conv.quest:
                print(f"{fname}:Could not find quest, good luck; finding it if it had any")
                
                num = Conversation.objects.filter(title__contains=questless_token).count()
                conv.title = f"{questless_token} ({num})"
                conv.is_quest = False
                
                print(f"{fname}: Conversation is now called {conv.title}")
                
                
            elif quest_step == 0:
                
                siblings = Conversation.objects.filter(quest=conv.quest)
                num = siblings.count()
                conv.title = f"{conv.quest.title} - Part ({num})"
                
                print(f"{fname}: Conversation is now called {conv.title}")
        else:
            if nameless_token in conv.title:
                print(f"{fname}: this already is a nameless function, you should change that! u.ú")
            else:
                nameless_list = Conversation.objects.filter(title__contains=nameless_token)
                conv.title = f"{nameless_token} [{nameless_list.count()}]"
        #todo: if you want to go overboard, query characters on possible speeches lol
        
    else: #? database has name marked as unique, so you don't need to worry
        print(f"{fname}: Conversation already has a name ({conv.title}")
    
    return conv.save()

def create_speech_name(conv,reply_to=None): # create names for speeches
    if reply_to is not None: #? careful, this can break
        num = 0 + Speech.objects.filter(previous_speech=reply_to).count()
        name = f"{reply_to.name}{ascii_uppercase[num]}"
        
    elif conv.is_linear: #? careful: replies can happen before conv is marked as non-linear
        letter = ascii_uppercase [ Speech.objects.filter(conversation=conv.id).count() ]
        name = f"{letter}"
        
    else:
        
        name = f"{conv.title}: Orphan !!!!"
        
        msg("create_name was called to non-linear and reply-less. Check {conv.title}","ODD")
    return name





# --------------------------------------------------------------------



def has_first_speech(conv,return_speech=False):
    """Checks if an object has a first speech or not
    Returns False if it doesn't have one
    Returns True if it has
    Returns Speech Object if it has one and return_speech was flagged true
    
    """
    if type(conv) is not Conversation:
        conv = get_object_or_404(Conversation, id=conv)
    
    
    try:
        if (first_speech := Speech.objects.filter(conversation=conv, is_first=True)):
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

def same_conv(speech):
    fname = "\n \033[33m same_conv \033[0m"
    fn_intro("same_conv", "validation")
    
    nxt = speech.next_speech
    prev = speech.previous_speech
    same = False
    
    
    if (speech.conversation == nxt.conversation or nxt is None) and (speech.conversation == prev.conversation or prev is None):
        same = True
        print(f"{fname}: All Okay")
    else:
        print(f"""{fname}: Conversations do not match
              
              Previous Speech [{prev}] is part of [{prev.conversation}]
              
              Speech [{speech}] is part of [{speech.conversation}]
              
              Next Speech: Speech [{nxt}] is part of [{nxt.conversation}]
              
              
              !!! Breaking [{speech.conversation}]
              """
              )
        break_conv(speech.conversation)
    
    return same
    
    
                     
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
    fname = "\n \033[33m give_last_speech \033[0m"
    fn_intro("give_last_speech", "validation")
    
    #todo maybe make a check if it is a Speech object or a string
    conv = get_object_or_404(Conversation,id=conv_pk)
    
    if conv.broken_chain:
        msg(f"{fname}: Conversation is broken. Sort your poopoo together")
        return False#, False

    
    if conv.is_linear:
        #? Rememeber: the following query only works if the code is linear
        try:
            
            #! Consider change this if you add next_speech (it will be objects.filter(next_speech=None))
            last_speech = Speech.objects.filter(
                conversation=conv_pk,
                replies__isnull=True #? "replies" here is the related_name for previous_speech
                )
            
            if last_speech:
                
                print(f'{fname}: Linear speech, trying to find last') 
                pprint.pprint(last_speech)
                print ('\n\n')
                
                return last_speech.first()#, True
        
        except Speech.MultipleObjectsReturned:
        
            msg(f"{fname}: Multiple Lasts, but marked as linear marking the conversation as broken")
            break_conv(conv_pk)
            
            return None#, False
        
        except Speech.DoesNotExist:
            
            #? The speech could be fullt cycled. Which is an infinite loop in-game
            #? More importantly, it shouldn't be marked as linear
            
            if not Speech.objects.filter(conversation=conv_pk):
                
                msg(f"{fname}: No posts, nothing wrong except the fact this function was called", "ODD")
                
                return (None, True) #? Empty new conversations are empty
            else:
                msg(f"{fname}: No lasts. Possible full cycle and infinite loop. Breaking conv for good measure")
                break_conv(conv_pk)
                
                return False#, False
        
    else:
        return None#, False
        
# def linear_check(conv_pk):
#     #? just for readability
#     last, linear = give_last_speech(conv_pk)
#     return linear

def cycle_check(speech, send_list=False):
    fname = "\n \033[33m cycle check \033[0m"
    #? add intro
    
    confluents = Speech.objects.filter(next_speech=speech)
    
    if not confluents: #? if no results
        print(f"{fname} [{speech}] has no speeches leading to it")
        #? unlikely to run on the final product, save for first_speeches
        
        return False
    
    elif (confluents.count() == 1) and (prev := confluents.first() == speech):
        print(f"{fname} [{speech}] has only {prev} leading to it (linear node)")
        
        #? you can validate previous_speech here. But it is better not to
        
        return False #? They seem to be linear
    
    else: 
        
        for conflu in confluents:
            if speech.previous_speech == conflu:
                print(f"{fname}: [{speech}] has a linear connection to [{conflu}]")
                continue
            if not conflu.next_is_cycled:
                print(f"{fname}: [{conflu}] cycles back to [{speech}], but is not marked as a cycle back. Fixing that")
                
                conflu.next_is_cycled = True
                conflu.save()
            else:
                print(f"{fname}: [{conflu} cycles to [{speech} as expected] ")
        
        if send_list:
            return confluents
        
        #? you can also maybe add an edit and then return a speech.save()
        return True
    

def linear_check(conv):
    # ! Warning, this does not check next_speech.
    
    fname = "\n \033[33m linear check \033[0m"
    fn_intro("linear check", "validation")

    if type(conv) is not Conversation:
        conv = get_object_or_404(Conversation, id=conv)
    
    # ------------------------
    linear = True
    speech = has_first_speech(conv,True)

    while linear:
    
        forks = Speech.objects.all(previous_speech = speech)
        
        count = forks.count()
        if count == 0: #? end of linear speech
            
            print(f"{fname}: {conv} is linear and ends at {speech}.")
            break
        
        elif forks.count() > 1: #? if there are forks, it is not linear
            
            linear = False
            
            print(f"{fname}: {conv} is not linear when it gets to {speech}.")
            pprint.pprint(forks)
            
            if conv.is_linear:
                print(f"{fname}: {conv} was not previously marked as linear. Fixing it.")
                conv._is_linear = False
                conv.save()
            
        else:           #? if there is only one result, it is linear, keep going
            speech = forks.first() 
    
    return linear


#TODO: use has_fork, is_fork, and check for empty fork questions

def validate_reply(speech, distrust_conv = False):
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
    
    #? Function log data --------------------------------------
    print("\n\n")
    fname = "\n \033[33m validate_reply \033[0m"
    #pprint.pprint(speech.conversation.description)
    print ("--------------------------------------")
    
    
    #? Set up --------------------------------------
    
    conv = speech.conversation
    #last_speech, linear = give_last_speech(conv.id)
    last_speech = give_last_speech(conv.id)
    
    if distrust_conv:
        linear = linear_check(conv) #? this function is harmless on single submits but heavy and redundant on conversation checks
    else:
        linear = conv.is_linear
    
    
    #? Name handling --------------------------------------
    
    if "!Auto!" in speech.name: #? this will have a chance to break until linear function check is made
        print(f"{fname}: Automatic name procedure ")
        speech.name = create_speech_name(conv,speech.previous_speech)
        print(f"New name: {speech.name}")
    
    #? Actual validation --------------------------------------
    
    
    #? Short next speech check
    
    if speech.next_speech:
        if speech.next_speech.previous_speech == speech:
            print(f"{fname}: {speech} and {speech.next_speech} reference each other")
            speech.next_is_cycled = False #? seems redundant but edits can change this value
        else:
            print(f"{speech.previous_speech} has {speech.next_speech.previous_speech} assigned instead of {speech}")
            print(f"{fname}: marking {speech} as next_is_cycled")
                    
            speech.next_is_cycled = True
            #todo create a field for the next_speech that is marked as "is_merge" or something
            
    #? Previous hierarchy handling (AKA the important stuff)
        
    if speech.previous_speech is None: #? Considering to be first speech of conversation
        print(f"{fname}: previous speech is none") 
        
        if not has_first_speech(conv.id): #? If there is no first speech, means this one is indeed the first
            
            print(f"{fname}: No first speeches. Saving")
            
            speech.is_first = True
            speech.save()
            
            return speech
        
        elif last_speech: #? linear creation form should not be obligated to add previous_speech.
                          #?This prevents any change there not be validated
                 
            if last_speech.id == speech.id: #? the prevents a false positive that does not let edit single speech conversations.
                print(f"{fname} Edit detected:")
                print(f"last (linear): {last_speech.id} \n submitted:     {speech.id}")
                print("------")
                
                speech.save()
                return speech
            
            print(f"{fname}: linear, saving [{speech}] as a reply to [{last_speech}]")
            
            speech.previous_speech = last_speech #? correctly fills a previous speech and places it on the end of the line
            speech.save()
            
            if not last_speech.next_speech: #? if conversation is linear and this is empty, it saves there
                last_speech.next_speech = speech #? this is not necessary for most hierarchies here, but it can be important on .yarn compiling
                last_speech.save()
            
            elif last_speech.next_speech == speech:
                print(f"{fname}: last speech [{last_speech}] already has {speech} assigned as next") #? possible edit?
                
                
            else: #? Consider using the cycle_check function instead.
                ...
                
            speech.save()
            return speech
        else:
            # todo: maybe deal with orphans here?
            msg(f"{fname} Odd scenario, not saving speech")
            
            return False
        
    #? Dealing with non-linear speeches -----------------------------------------------------------------------------
    elif not linear and speech.previous_speech is None: #it can't index it at all
        print(f"{fname}: [{speech}] has no previous_speech when {conv} is non-linear conversation.\n Not saving it")
        return False
            
    else:
        parent = speech.previous_speech #? Sets up for the rest of the code below
    
    print(f"{fname}: [{speech}] has previous_speech ( {speech.previous_speech})")
    
    forks = Speech.objects.filter(previous_speech=parent)
    if (forks.count() == 1) and forks.first() is speech: #? Likely an edit detecting itself.
                                                        #? just because conversation is non-linear, doesn't mean all speeches branch
        print(f"{fname} [{speech}] is being saved")
        speech.save()
        parent.next_speech = speech #? this is triggered also on conversations self.checks
        parent.save()
        return speech
    
    else: 
        for fork in forks: #? in case the others don't know yet they're a fork, they do now
            fork.is_fork = True
            fork.save()
        
        parent.next_speech = None #? if child wasn't in the loop you have bigger problems
        parent.has_fork = True #todo: considering this is outdated by now
        
        speech.is_fork = True #? for good measure
        conv.is_linear = False #? same here
        
        
        conv.save()
        parent.save()
        speech.save()
    

    return speech

def conv_self_check(conv):
    ...