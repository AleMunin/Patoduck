
def linear_check(conv,ret_obj=False,flag=False):
    # ret_obj = Returns object if asked
    # flag = flags as broken chain
    # Returns None if Broken
    # Returns False if not linear
    # Returns True if Linear

    print("")
    print (f"Conversation [{conv.title}] will have a linearity check")
    if conv.is_linear is True:
        print(f"Conversation claims to be linear")
    else:
        print("Conversation claims to not be linear")

    if ret_obj is True:
        print ("Linear check will return the end of line")
    if flag is True:
        print("Linear check will flag if Conversation is broken")
    
    try:
        first_speech = Speech.objects.get(conversation=conv.id, is_first=True)
        print(f"    First speech found")

        loop = 1
        end_of_line = False
        broken = False
        nxt_in_line = None
        current_line = None

        while end_of_line is False:
            print(f"    {loop}")
            if loop == 1:
                current_line = first_speech
                print(f"    First speech assigned in the loop")
            else:

                try:
                    
                    nxt_in_line = Speech.objects.get(id = current_line.next_speech)

                    print(f"    current line is {current_line.name}")
                    print(f"    .next_speech is: {current_line.next_speech}")
                    print(f"    next in line is {nxt_in_line.name}")
                    current_line = nxt_in_line
                except Speech.DoesNotExist:
                    print (f"   This is the last in chain")
                    end_of_line = True
                    break
                
            
            loop +=1

            if current_line.has_fork or current_line.is_fork:
                
                if conv.is_linear:
                    print(f"    Conversation IS NOT LINEAR, but claims to be")
                    if flag:
                        conv.broken_chain = True
                        conv.save()
                    return None
                else:
                    print(f"    Indeed Not linear")
                    return False
            

        if end_of_line is True:
            print(f"    Speech is linear")
            if not conv.is_linear:
                print(f"   But it claimed to be forked")
                return None
            
            if ret_obj:
                print(f"    Will be returning the object")
                return nxt_in_line
            else:
                print(f"    Will be returning true")
                return True



    except first_speech.DoesNotExist:
        print("Conversation has no speeches marked as first")
        # if you really want you can do a query check if it is the only object and return True or None
        return True
    except first_speech.MultipleObjectsReturned:
        print("Conversation has MULTIPLE first speeches")
        if flag is True:
            conv.broken_chain = True
            conv.save()
        return None


    

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


def validate_new_speech(speech,conv,returnme=False):
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

    else: # If there are other conversations

        # (LINEAR) If just wants to be on the end of the line 
        if speech.is_fork is False and speech.previous_speech is None:
            print ("Speech has no fork and has no previous, should be added on the end of the line")
            
            #conv_stats = linear_check(conv,False,True)

            if conv_stats is None: #if error
                print("Conversation has broken chain") 
                broken = True #it was already flagged, but for good measure

            elif conv_stats is True: #if it is linear
                try:                    
                    last_in_line = Speech.objects.get(conversation = conv.id, next_speech=None)

                    print (">>>>>> Speech added to the end of the line.")
                    speech.previous_speech = last_in_line
                    speech.save() # has to be saved before altering speech
                    last_in_line.next_speech = speech
                    last_in_line.save()
                    valid = True
                except Speech.MultipleObjectsReturned:
                     print("!!!!!! Somehow got several next_speech free results in a linear conv")
            else: # Conv is not linear, so this shouldn't happen
                print("!!!!! Conversation is NOT linear. Speech is not a fork, Speech has no specific previous either")
                print("!!!!! Speech is not valid therefore it will not be saved")
                speech_status(speech)

        ## (LINEAR) Specific reply to a .previous_speech 
        elif speech.is_fork is False and speech.previous_speech is not None: 
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
                    elif letter_check is speech:
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
            return False 
            
        print("Speech is valid, will return True after save")
        speech.save()
        conv.save()

        if returnme is True:
            print("")
            return speech
        else:
            print("")
            return True
    else:
        print("Speech is not valid, will return False after save")
        return False