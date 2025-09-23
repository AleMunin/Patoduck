from .models import *

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

def tree_of_speeches(conv_pk,orphans=False):
    """
    Iterates a query and packages the hierarchy trees
    Then it will query orphans, if set to do it
    """
    all_speeches = []
    current_speech = []
    
    first_speech = Speech.objects.filter(conversation=conv_pk, is_first=True)
       # TODO: if result is more than one, flag as broken broken_chain, exit
    
    if not first_speech: # ? if queryset is empty
        if test_speeches := Speech.objects.filter(conversation=conv_pk): #? if there are speeches
            flag_conv = Conversation.objects.get(id=conv_pk)
            flag_conv.broken_chain=True 
            #TODO: LOG this properly
        else:
            #TODO: LOG this properly
            msg = """
            
            The conversation asked to edit is just empty, don't worry.
            
            """
            print(msg)
            
    else:
            
        all_speeches.append(first_speech)
        
        current_speech += first_speech #? will add as a single element of the list
        speeches = Speech.objects.filter(previous_speech=first_speech.id)
        
        for speech in speeches:
            
            forks = Speech.objects.filter(previous_speech=speech.id)
            for fork in forks:
                all_speeches.append(forks)
            all_speeches.append(speeches)
        
        return all_speeches
    
    
    # query orphans
    # exclude is_first
    return None
    