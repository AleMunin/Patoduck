from django.shortcuts import get_object_or_404, render, redirect
# from django.urls import reverse
# from django import forms 
# from django.forms import ModelForm 

from .models import *
from .forms import *

from pprint import pprint

import secrets #for hash

# QUALITY OF LIFE

def get_fork_fields(obj,language_group): # management of my own madness
    speech = obj

    match language_group:

        case "all": # does not return the ids, though
            my_initials = { #thank god alt + click can copy paste properly
            
                'fork_question_en_A' : speech.fork_question_en_A, 
                'fork_question_pt_A' : speech.fork_question_pt_A, 
                'fork_question_es_A' : speech.fork_question_es_A, 
                
                'fork_question_en_B' : speech.fork_question_en_B,
                'fork_question_pt_B' : speech.fork_question_pt_B,
                'fork_question_es_B' : speech.fork_question_es_B,

                'fork_question_en_C' : speech.fork_question_en_C,
                'fork_question_pt_C' : speech.fork_question_pt_C,
                'fork_question_es_C' : speech.fork_question_es_C,

                'fork_question_en_D' : speech.fork_question_en_D,
                'fork_question_pt_D' : speech.fork_question_pt_D,
                'fork_question_es_D' : speech.fork_question_es_D,

                'fork_question_en_E' : speech.fork_question_en_E,
                'fork_question_pt_E' : speech.fork_question_pt_E,
                'fork_question_es_E' : speech.fork_question_es_E,

                'fork_question_en_F' : speech.fork_question_en_F,
                'fork_question_pt_F' : speech.fork_question_pt_F,
                'fork_question_es_F' : speech.fork_question_es_F,

            }

        case "ids":
            my_initials = {
                "fork_speech_AA" : speech.fork_speech_AA,
                "fork_speech_BB" : speech.fork_speech_BB,
                "fork_speech_CC" : speech.fork_speech_CC,
                "fork_speech_DD" : speech.fork_speech_DD,
                "fork_speech_EE" : speech.fork_speech_EE,
                "fork_speech_FF" : speech.fork_speech_FF,
            }

        case "en":
            my_initials = { #thank god alt + click can copy paste properly
            
                'fork_question_en_A' : speech.fork_question_en_A, 
                
                'fork_question_en_B' : speech.fork_question_en_B,
                
                'fork_question_en_C' : speech.fork_question_en_C,
                

                'fork_question_en_D' : speech.fork_question_en_D,

                'fork_question_en_E' : speech.fork_question_en_E,

                'fork_question_en_F' : speech.fork_question_en_F,
                

            }

        case "pt":
            my_initials = { #thank god alt + click can copy paste properly
            
                'fork_question_pt_A' : speech.fork_question_pt_A, 
                
                'fork_question_pt_B' : speech.fork_question_pt_B,

                'fork_question_pt_C' : speech.fork_question_pt_C,

                'fork_question_pt_D' : speech.fork_question_pt_D,

                'fork_question_pt_E' : speech.fork_question_pt_E,

                'fork_question_pt_F' : speech.fork_question_pt_F,

            }

        case "es":
            my_initials = { #thank god alt + click can copy paste properly
             
                'fork_question_es_A' : speech.fork_question_es_A, 
                
                'fork_question_es_B' : speech.fork_question_es_B,


                'fork_question_es_C' : speech.fork_question_es_C,

                'fork_question_es_D' : speech.fork_question_es_D,


                'fork_question_es_E' : speech.fork_question_es_E,

                'fork_question_es_F' : speech.fork_question_es_F,

            }
        case "A":
            my_initials = { #thank god alt + click can copy paste properly
            
                'fork_question_en_A' : speech.fork_question_en_A, 
                'fork_question_pt_A' : speech.fork_question_pt_A, 
                'fork_question_es_A' : speech.fork_question_es_A, 

            }
        case "B":
            my_initials = { #thank god alt + click can copy paste properly
            
                
                'fork_question_en_B' : speech.fork_question_en_B,
                'fork_question_pt_B' : speech.fork_question_pt_B,
                'fork_question_es_B' : speech.fork_question_es_B,

            }
        case "C":
            my_initials = { #thank god alt + click can copy paste properly

                'fork_question_en_C' : speech.fork_question_en_C,
                'fork_question_pt_C' : speech.fork_question_pt_C,
                'fork_question_es_C' : speech.fork_question_es_C,

            }
        case "D":
            my_initials = { #thank god alt + click can copy paste properly

                'fork_question_en_D' : speech.fork_question_en_D,
                'fork_question_pt_D' : speech.fork_question_pt_D,
                'fork_question_es_D' : speech.fork_question_es_D,

            }
        case "E":
            my_initials = { #thank god alt + click can copy paste properly


                'fork_question_en_E' : speech.fork_question_en_E,
                'fork_question_pt_E' : speech.fork_question_pt_E,
                'fork_question_es_E' : speech.fork_question_es_E,

            }
        case "F":
            my_initials = { #thank god alt + click can copy paste properly

                'fork_question_en_F' : speech.fork_question_en_F,
                'fork_question_pt_F' : speech.fork_question_pt_F,
                'fork_question_es_F' : speech.fork_question_es_F,

            }
    return my_initials

# VALIDATION


def ugh_validate_speech(speech,conv): #both arguments have to be models
    print(f"Validating for [{conv.title}]")
    conv_speeches = Speech.objects.filter(conversation=conv.id)
    if speech.previous_speech is None:  #possible new linear
        if conv_speeches is False: # if conv is empty
            speech.is_first = True
            print(f"New First Speech: [{speech.name}]")
        elif conv.is_linear is True:
            print(f"Conversation is Linear")
            
            first_speech = None
            
            for single_speech in conv_speeches:
                if single_speech.has_fork is True: # should be linear
                    break

                if single_speech.is_first is True:
                    first_speech = single_speech
                    break


            if first_speech is None: # if you can't even find the first, you have bigger problems
                print(f"First Speech is not assigned among other speeches. This is a Broken chain")
                conv.broken_chain
            else:
                if first_speech.next_speech is None:
                    print("Saving Speech as Second Speech")
                    speech.save()
                    first_speech.next_speech = speech
                    first_speech.save()
                else:
                    print(f"Looking for the end of the line")
                    nxt_in_line = Speech.objects.filter(id=first_speech.next_speech)
                    end_of_line = False
                    loop_count = 0
                    while end_of_line is False:
                        if loop_count > 0:
                            nxt_in_line = Speech.objects.filter(id=nxt_in_line.next_speech)
                        loop_count +=1

                        if nxt_in_line.has_fork is True or nxt_in_line.is_fork is True:
                            print("!!!!! Unexpected fork assignment at {nxt_in_line.name}. Flagged as Broken Chain")
                            conv.broken_chain = True
                            conv.save()

                        if nxt_in_line.next_speech is None:

                            speech.previous_speech = nxt_in_line.id
                            nxt_in_line.next_speech = speech.id
                            speech.save()
                            nxt_in_line.save()
                            print(f"Found the end of linear conversation after {loop_count} attempts. They have been assigned")
                            break

        else: #broken beyond repair
            # Reason being that conversation should not be flagged as linear.
            # If it is not linear, this speech should have a previous speech assigned.
            print("This speech has no PREVIOUS assigned to it")
            print("And conversation IS NOT LINEAR")
            print("This means Fork form should have assigned a primary key")
            print("Conversation has been flagged as Broken")

            conv.broken_chain = True
            
        
    else:  #if it has a previous speech assigned
        try:
            reply_to = get_object_or_404(Speech, id=speech.previous_speech)
            print(f"This is a reply to {reply_to.name}")
        except:
            print(f"The key {speech.previous_speech} this form is assigned to does not exist.")
        
        if reply_to.has_fork is False: # Checks if previous is linear
            if reply_to.next_speech is None:
                speech.save()
                reply_to.next_speech = speech
                reply_to.save()
                print("Reply to had no previous speech, speech was assigned to it")
            elif reply_to.next_speech == speech:
                print("Nothing to do here, both reply to and speech match each other")
            elif reply_to.next_speech != speech:
                print("LINEAR reply to has another speech assigned to it. Flagged as broken chain")
                print("This can be fixed by making both of them forks")
                conv.broken_chain = True
            else:
                print("I don't know what went wrong in here. but it was VERY WRONG")
                conv.broken_chain = True

        else: # Loops through the fork fields until it finds a place
            speech.is_fork = True #Properly signals
            conv.is_linear=False # properly signals
            fields = get_fork_fields(reply_to,"ids")
            
            print(f"Reply to [{reply_to.name}] has forks.")

            if speech.fork_letter is None: #if fork letter is empty
                print(f"Speech being validated has no fork letter")

                found = False
                for key, field in fields.keys():
                    if field == speech: #if it was already assigned
                        speech.fork_letter = key
                        found = True
                        print ("Found exact match on letter fields")
                        speech.fork_letter = key
                        speech.save()
                        break
                    # elif field is None: # How can you be sure this fork is from here?
                    #     speech.fork_letter = key
                    #     speech.save()
                    #     setattr(reply_to, key, speech) #will set the field
                    #     found = True
                    #     reply_to.save()
                    #     break
                if found is False:
                    print("Found no matches. Flagged as broken chain")
                    conv.broken_chain = True
            else: # check if t hey are the same
                print("Speech being validated has fork letter: {speech.fork_letter}")
                letter_check = getattr(reply_to, speech.fork_letter)
                if letter_check is None:
                    print("Letter field was empty, assigning it.")
                    setattr(reply_to, letter_check, speech)
                    reply_to.save()

                elif (speech == letter_check):
                    print("Fork field was already previously assigned.")
                else:
                    print("Letter Fork from Speech does not match its reply")
                    print("Flagging conversation as broken chain")
                    conv.save()

        reply_to.save() # just for good measure.

    # Call function to name convention

    if speech.line_hash is None:
        print("Assigning hash for speech")
        speech = create_hash(speech)

    # generate line hash
    #conv.total_speeches += 1 (you need to make an if statement to know if it was't there already)

    conv.save()
    speech.save()

    return speech


def in_list (obj, obj_list): # checks if object is on list
    for item in obj_list:
        if item == obj:
            return True
    return False


# GENERATION

def create_hash(speech=None):    #generate hexadecimal of 6 digits and checks if it is unique, DOES NOT save.
    unique = False
    hex = secrets.token_hex(3)
    while unique is False:
        if not Speech.objects.filter(line_hash=hex):
            unique = True
        else:
            hex =  secrets.token_hex(3)
    else:
        if speech is not None:
            speech.line_hash = hex
            return speech
        else:
            return hex
    

def create_name(conv,reply_to=None): # create names for speeches
    if conv.is_linear:
        name = f"{conv.title} [{len(Speech.objects.filter(conversation=conv.id))}]"
    elif reply_to is not None:
        num = len(Speech.objects.filter(previous_speech=reply_to))
        num += 1
        name = f"F-{reply_to.name} [{num}]"
    return name



# SORTING

def glob_forks(speech,audit): #recursive sort by query of speeches, puts them right next to the branching parent
    # audit is the overall list, it prevents infinite loops & missing items
    
    sorted_forks = []   #note: it will NOT add og "speech" to the list.
    cycle_risk = False
    forks = Speech.objects.filter(previous_speech = speech.id) #should work for linear AND forks
    if not forks.exists(): # failsafe
        forks = Speech.objects.filter(id = speech.next_speech) #always one result.
    

    if forks.exists() and cycle_risk is False:
        for fork in forks:
            cycle_risk = in_list(forks,audit)
            if cycle_risk is False:
                sorted_forks.append(fork)
                sorted_forks = sorted_forks + glob_forks(fork,sorted_forks)
    
    return sorted_forks


def sort_speeches (conv): # Sorts by query because fuck finding token in object lists
    # seriously how did i not get tutorials on this when everything is an object in python, what am i missing?

    
    first_speech = Speech.objects.filter(conversation=conv.id, is_first=True)
    if not first_speech.exists(): # Report conv as broken or empty
        if conv.total_speeches > 0:
            conv.broken_chain = 0
            conv.save()
        else:
            print (f"sort_speeches: {conv.title} is empty.")
        return None

    current_speech = first_speech
    sorted_speeches = []

    sorted_speeches.append(current_speech)
    sorted_speeches = sorted_speeches + glob_forks(current_speech,sorted_speeches)

    return sorted_speeches



# TESTS -------------------------------------


    

def speech_status(speech):
    print("")
    print("")
    print("------------------------")
    print("I'm Speech {speech.name}, my id is ({speech.id})\n\n")
    
    conv = Conversation.objects.filter(id=speech.conversation)
    speaker = Character.objects.filter(id=speech.speaker)

    print(f"My speech is {conv.title}")
    print(f"My Speaker is: {speaker}")

    if speech.line_hash is None:
        print("I do not have a Hash")
    else:
        print(f"My Hash is: {speech.line_hash}")

    if speech.txt_pt is None:
        print(f"I have no PT text")
    if speech.txt_es is None:
        print(f"I have no ES text")

    if speech.is_first is True:
        print("I am the first of my Conversation\n")
        if (speech.previous_speech != None):
            print(f"!!!!! But I do have a previous speech")
        if speech.is_fork is True:
            print("!!!!! But I am also a  fork")

    if (speech.previous_speech != None):
        prev = Speech.objects.filter(id=speech.previous_speech)
        print(f"My previous speech is {prev.name} ({prev.id})")

        if prev.has_fork is True:
            print("My previous speech has forks")
        else:
            print("!!!!! My previous speech has no forks")
            if prev.next_speech is None:
                print("Its next speech is null")
            elif prev.next_speech is speech.id:
                print("And it points right at me")
            else:
                print("My previous speech does not point right to me")

    if speech.next_is_cycled:
        print("I should cycle back to another speech")

    if (speech.next_speech != None):
        nxt = Speech.objects.filter(id=speech.next_speech)
        print(f"My next speech is {nxt.name}  ({nxt.id}))")
    else:
        print("I do not have a next speech")
    

    if speech.has_fork is True:  
        print("I have forks")
    
    print("-------------------------------")


def old_validate_new_speech(speech,conv):
    print("")
    print(f"Validating for [{conv.title}]")
    conv_speeches = Speech.objects.filter(conversation=conv.id)

    # Stats vars

    first_one = False #if was assigned to be the first
    broken = False #if conversation is broken
    valid = False #hopefully self explanatory in this function


    if not conv_speeches: # if no speeches at all, this is the first one
        speech.is_first = True
        print(f">>>>>> New First Speech: [{speech.name}]")
        first_one = True
        speech.save()
        valid = True

    elif conv.is_linear: # if it is linear
        try:
            last_speech = Speech.objects.get(conversation = conv.id, next_speech = None)
            speech.previous_speech = last_speech
            speech.save()
            last_speech.next_speech = speech
            last_speech.save()
        except Speech.DoesNotExist:
            print(f" Conversation has no free with next_speech object")
        except Speech.MultipleObjectsReturned:
            print(f"Multiple free objects returned, possible forks")
    else:
        ## (LINEAR) Specific reply to a .previous_speech 
        if speech.is_fork is False and speech.previous_speech is not None: 
            print("Speech has a specific linear response")
            # Technically this shouldn't happen, but maybe you can just copy paste the code
            # later to add to an edit validation or something.
            reply_to = get_object_or_404(Speech, id=speech.previous_speech)

            if reply_to.next_speech is None and reply_to.has_fork is False: #no harm there
                speech.save() #validate itself on the database
                reply_to.next_speech = speech
                reply_to.save()
                print(f">>>>>> New Speech has been added as a response to {reply_to.name}")
                valid = True

            elif reply_to.next_speech is not None:
                if reply_to.next_speech is speech:
                    print("!!!!!! This is a new speech function but somehow speech was already registered")
                    
                else:
                    print(f"!!!!!! Reply to {reply_to.name} was impossible because it already had something next in line")
                    print("Speech will not be saved. Try forking next time")

        
        # (FORKs) if it has forks to something
        elif speech.is_fork is True and speech.previous_speech is not None: 
            print ("Speech is pointing out it is a fork to something")

            reply_to = get_object_or_404(Speech, id=speech.previous_speech)

            if reply_to.has_fork is False:
                print("!!!!!! Reply to Speech is impossible because it has no forks")
            else:
                if speech.letter_check is not None:
                    letter_check = getattr(reply_to, speech.fork_letter) # will throw an error if empty

                    if letter_check is None: # if the value of that field is empty
                        speech.save() #make it valid on the database
                        setattr(reply_to, letter_check, speech)
                        reply_to.save()
                        valid = True
                    elif letter_check is Speech:
                        print("!!!!! New speech function found speech to already exist on {reply_to.fork}")
                        print("No saves will be done, but check what is happening on admin")
                        print("Reply to:")
                        speech_status(reply_to)
                        print("Speech forked:")
                        speech_status(speech)


        # Massive error
        else: # something very wrong happened
            print("Something very wrong happened on the validation. Speech will not be saved")

            speech_status(speech)

    # Stats handling

    if valid is True: # can still return false

        if speech.line_hash is None:
            print("Assigning hash for speech")
            speech = create_hash(speech)
            

        if first_one is True:
            if speech.previous_speech is not None:
                broken = True

        if speech.has_fork is True:
            conv.is_linear = False
            print(">>>>>> Speech has fork signaling, Conversation no longer linear")

        if broken is True:
            print (">>>>>> Assigning as broken chain")
            conv.broken_chain = True
            conv.save()
            print("")
            # will not save speech by itself, but others above might
            
        print("Speech is valid, will return True after save")
        speech.save()
        conv.save()

        return (True, speech)
    
    else:
        return (False, speech)

def validate_new_speech(speech,conv,reply_to=None):

    print("")
    print(f"Validating for [{conv.title}]:  {speech.name}")
    conv_speeches = Speech.objects.filter(conversation=conv.id)
    
    linear = conv.is_linear #because the propety itself might change through this
    valid = False
    bare_minimum = True


    #-------------------------------------
    # Minor safety checks
    if not isinstance(speech,Speech):
        print(f"!!!!! {speech} not a Speech")
        bare_minimum = False


    if not isinstance(conv,Conversation):
        print(f"!!!!! {conv} not a Conversation")
        bare_minimum = False

    print("")
    print(f" VALIDATING NACHOOOOOOOOOOOOOOOOOOS")
    print("")
    print(f"{speech.conversation}")


    if speech.conversation != conv:
        print(f"!!!!! {speech} is not assigned to {conv} but to {speech.conversation}")
        bare_minimum = False

    if reply_to is not None:
        if not isinstance(reply_to,Speech):
            print(f"!!!!! Reply to, {speech} not a Speech")
            bare_minimum = False
        if reply_to.conversation != conv:
            print(f"    !!!!! Reply to does not share {conv}, it belongs to {reply_to.conversation}")
            bare_minimum = False



    if not bare_minimum:
        print(f"Somehow this didn't reach the bare minimum, returning false")
        return False, speech
    

    #-------------------------------------

    # Minor adjustments (save conv.save only in the end)

    if conv.is_linear and speech.has_fork:
            conv.is_linear = False
    
    #-------------------------------------
    #           EMPTY Check

    if not conv_speeches: # if empty conv
        speech.is_first = True
        valid = True # just in case I change and forget
        print(f">>>>>> New First Speech: [{speech.name}]")
        first_one = True

        speech.save()
        conv.save()
        return True, speech

    # -------------------------------------
    #           LINEAR Check

    elif not speech.is_fork and linear:
        try:
            last_speech = Speech.objects.get(conversation=conv.id, next_speech=None)

            speech.previous_speech = last_speech
            speech.save()
            last_speech.next_speech = speech
            last_speech.save()

            valid = True
        
        except Speech.DoesNotExist:
            print(f"    !!!!! No free next_speeches")
        except Speech.MultipleObjectsReturned:
            tests = Speech.objects.filter(conversation=conv.id, next_speech=None)
            
            print
            print(f"    !!!!! Linear Speech has many free next_speeches")

            for obj in tests:
                pprint(obj)
                pprint(f"   {obj.next_speech}")

            print("")

    #-------------------------------------
    #           Fork Check

    # elif speech.is_fork and not linear:
    #     if reply_to is None:
    #         print(f"    !!!!! {speech} is a fork, but function was not given a primary key from what is branching of")

    #     else:
    #         if reply_to.next_speech is not None or reply_to.has_fork is False:
    #             pprint(f"   !!!!! {reply_to} is configured to be linear. Splitting branches need to be configured to haveforks first")
    #             pprint(f"   next_speech: {reply_to.next_speech}")
    #             pprint(f"   has_fork: {reply_to.has_fork}")
    #         else:
    #             if speech.fork_letter is not None:
    #                 letter_check = getattr(reply_to, speech.fork_letter) # will throw an error if empty

    #                 if letter_check is None: # if the value of that field is empty
    #                     speech.save() #make it valid on the database
    #                     setattr(reply_to, letter_check, speech)
    #                     reply_to.save()
    #                     valid = True

    #                 elif letter_check is speech:
    #                     print(f"    !!!!! New speech function found speech to already exist on {reply_to.fork}")
    #                     print(f"    No saves will be done, but check what is happening on admin")
    #                     print(f"    Reply to:")
    #                     speech_status(reply_to)
    #                     print(f"    Speech forked:")
    #                     speech_status(speech)
    #                 else:
    #                     print(f"    !!!!! That slot is full with something else:")
    #                     print(f"         {letter_check}")

        
    if valid:
        print (f"    {speech} was valid and saved into the database.")

        if speech.line_hash is None:
            speech.line_hash = create_hash()

        speech.save() # this HAS to be repeated before so other things receive its pk

        conv.save() # avoid using this on the code, though


    # if speech.is_fork and reply_to=None:
    #     print(f"    Invalid, has fork but no primary key")
    #     return False
    # elif not 
    #-------------------------------------
    
    return valid, speech