
def og_validate_speech(conv_pk,form,reply_to=None): # Pick what is useful and delete after
    # assumes post was confirmed
    # NEEDS a form request from post, and that the form was valid
        # It does check form.is_valid here, but just throws a wrench so I can wake up about it, in case
        # I call this without doing it.
    # Needs a conversation to exist beforehand
    # Reply_to can either be a None or a Speech.id
    


    # maybe make it optional for be speech pk o a second argument?
    # assumes you got the pk from a get_object_or_404.
    # Call would be like:
    # if request.method == 'POST':
    #   validate_speech(conv_pk, SpeechCreateForm(request.POST), speech_pk )
    

    conv = get_object_or_404(Conversation,id=conv_pk) #get conversation

    if form.is_valid():
        conv_speeches = Speech.objects.filter(conversation=pk) # get before having this one on the list
        speech=form.save(commit=False)


        if reply_to is not None: # If definitely know who you'r replying to.

            og_speech = get_object_or_404(Speech,id=reply_to)

            speech.previous_speech = reply_to

            if (og_speech.has_fork is False) and (og_speech.next_speech is None or og_speech.next_speech is speech.id):
                # this means it is a reply to something.
                og_speech.next_speech = speech.id

            else: # It will deal with it
                add_as_fork(og_speech,speech,conv) # it will comment the problem there too

            og_speech.save()
            speech.save()

        elif not conv_speeches.exists(): # if no other speeches, this is the first

            speech.is_first = True
            speech.save()

        else: # ASSUMES THE CONVERSATION IS LINEAR, and this is a response.
            first_speech = None
            
            for single_speech in conv_speeches: # Sorts to find a is_first

                if single_speech.id is speech.id: continue # just good measure

                if single_speech.is_first is True:
                    next_chain = first_speech = single_speech.id
            
            # Once it knows where to start, it will loop the chain of foreign keys, looking
            # for the last one, which will have the next_speech field as null.
            # objects.get raises an exception in case the key is invalid for whatever reason.
            # It also register if it ever finds a fork
            #   (If there is ever a fork in a conversation, all following replies should have a reply_to key)

            while next_chain is not None: # canibalize this for a chain verification
                try: 
                    next_speech = Speech.objects.get(id=next_chain)

                    if next_speech.has_fork is True:
                        next_speech.comment = f" {next_speech.comment} [!!  There shouldn't be forks in this talk something went wrong !!]"
                        speech.comment = "[!! This was a linear reply but it got lost in a fork !!]"
                        
                        next_speech.save()
                        speech.save()

                        next_chain = None


                    else:
                        if next_speech.next_speech is None:
                            next_speech.next_speech = speech.id
                            speech.previous_speech = next_speech

                            next_speech.save()
                            speech.save()
                        else:
                            next_speech = next_speech.next_speech



                except:
                    next_chain = None
                    speech.comment = "[!! This speech was supposed to be on the end of a linear line, but something went wrong !!]]"
                
            speech.save()

            # if all the options have a fork, write a comment on this and save
            # maybe update the models on rogue lost speches


        speech.save()
        return speech
    return False # This will throw an ugly error

# ----------



def add_as_fork(og_speech,speech,conv): # pick what is useful and remove when you're done
    # Register id keys on its places and checks if the chain of foreign keys can break

    fork_validate = False

    # arguments are speech objects
    # if no slots on forks for that speech.
    # write on speech.commentary and on og_speech.commentary.

    if og_speech.has_fork is False and og_speech.next_speech is None: #if a honest mistake happened
        og_speech.has_fork = fork_validate = True

    else:
        og_speech.comment = "[!! This speech should be a fork but it isn't !!]" + og_speech.comment
        conv.description = "[!! This conversation has blank fork, check their comments !!]  " + conv.description
        speech.comment = "[!! This speech lis linked to an empty form !!] " + speech.comment

        # Any changes to correct this are better doe manually. At best write a log in here.

    if fork_validate:
        fork_slots = [og_speech.fork_speech_AA, og_speech.fork_speech_BB,og_speech.fork_speech_CC,og_speech.fork_speech_DD,og_speech.fork_speech_EE,og_speech.fork_speech_FF]
        found_a_fork = False
        #already_a_fork = False
        empty_slot = None

        for slot in fork_slots:

            if slot is speech.id:
                #already_a_fork = True # just if you need it.
                break
            if slot is None:
                empty_slot = slot
                found_a_fork = True

        if found_a_fork is False:
            speech.comment = "[!! This links to a speech with too many forks for the game !!]" + speech.comment
            conv.description = "[!! Some speeches have too many forks !!]" + conv.description
        else:
            empty_slot = speech.id

    og_speech.save()
    conv.save()
    speech.save()
