from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from django import forms 
from django.forms import ModelForm  # because apparently importing forms or * was not working.
# Create your views here.

# RUles of Thumb:

# Forms for those models are near their respective main views
# "process" functions can be registered as views, but are usually just HTMX responses
# functions not called views or processes are usually called by others


def home_view(request):

    #This view will be called only for chars, later down the line

    chars = Character.objects.all()
    quests = Quest.objects.all()
    locs = Location.objects.all()
    convs = Conversation.objects.all()
    speeches = Speech.objects.all()


    context ={
        "all_chars" : len(chars),
        'all_locs' : len(locs),
        "all_quests": len(quests),
        "all_convs" : len(convs),
        "all_speeches" : len(speeches)
    }

    return render(request,'site/home.html', context )


# Form Views ============================================================

# Character ----------------------------------------------------

class CharCreateForm(ModelForm):
    class Meta:
        model = Character
        fields = '__all__'


def character_create_view(request):
    form = CharCreateForm()

    if request.method == 'POST':
        form = CharCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request,'site/forms/char/create_char.html', {'form' : form })

def all_char_view(request):

    all_char = Character.objects.all()
    total_char= len(all_char)


    #check if conversations are part of a quest? idk

    return render(request, 'site/all_char.html', { "chars" : all_char, "total_char" : total_char } )

# Location ----------------------------------------------------

class LocationCreateForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

def location_create_view(request):

    if request.method == 'POST':
        form = LocationCreateForm(request.POST)
        if form.is_valid():
            form.save()
            
    form = LocationCreateForm()
    
    context = {
        "form" : form
    }
    return render(request, 'site/forms/loc/create_location.html', context)

def all_location_view(request):

    all_loc = Location.objects.all()
    total_loc= len(all_loc)

    context = {
        "all_loc" : all_loc,
        "total_loc" : total_loc
    }


    #check if conversations are part of a quest? idk

    return render(request, 'site/all_loc.html', context )

    
# Quest -----------------------------------------------------

class QuestCreateForm(ModelForm):
    class Meta:
        model = Quest
        fields = '__all__'

def quest_create_view(request):
    form = QuestCreateForm()

    if request.method == 'POST':
        form = QuestCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request,'site/forms/create_quest.html', {'form' : form })

def all_quest_view(request):
    all_quests = Quest.objects.all()
    total_quest = len(all_quests)

    return render(request, 'site/all_quests.html', { "quests" : all_quests, "total_quest" : total_quest } )

# Conversation & Speeches -----------------------------------------------------

class ConversationCreateForm(ModelForm):
    class Meta:
        model = Conversation
        fields = '__all__'

class ConversationEditForm(ModelForm): #edits the conversation, not the speeches
    class Meta:
        model = Conversation
        fields = ['title', 'is_quest', 'quest', 'quest_step', 'is_cutscene', 'condition','description']
        labels = {
            'body' : '',
        }

    # CONDITIONALS
    def __init__(self, *args, **kwargs): # there would be probably a better way but i can't be bothered
        super(ConversationEditForm, self).__init__(*args, **kwargs) #inheritance beurocracy

        #Those will toggle when "is quest is selected"
        self.fields['is_quest'].widget.attrs.update({'id': 'is_quest_conv'})
        self.fields['quest'].widget.attrs.update({
            'id'   : 'quest_select',
            'class': 'hidden_for_now'
            })
        self.fields['quest_step'].widget.attrs.update({
            'id'   : 'quest_step',
            'class': 'hidden_for_now'
            })
        


class SpeechCreateForm(ModelForm):
    class Meta:
        model = Speech
        fields = '__all__' #maybe remove that because we don't want the name or conversation

    #this way I don't need to know the default field type to add class

    def __init__(self, *args, **kwargs): # there would be probably a better way but i can't be bothered
        super(SpeechCreateForm, self).__init__(*args, **kwargs) #inheritance beurocracy

        # Regular

        self.fields['name'].widget.attrs.update({'class': 'speech_name'})

        # Hidden

        self.fields['txt_es'].widget.attrs.update({'class': 'speech_name hide_annoying_parent'})

        self.fields['previous_speech'].widget.attrs.update({'class': 'speech_name hide_annoying_parent'})
        self.fields['next_speech'].widget.attrs.update({'class': 'next_speech hide_annoying_parent'})

        self.fields['fork_question_en_A'].widget.attrs.update({'class': 'fork_A hide_annoying_parent'})
        self.fields['fork_question_pt_A'].widget.attrs.update({'class': 'fork_A hide_annoying_parent'})
        self.fields['fork_question_es_A'].widget.attrs.update({'class': 'fork_A hide_annoying_parent'})

        self.fields['fork_speech_AA'].widget.attrs.update({'class': 'fork_A hide_annoying_parent'})

        self.fields['fork_question_en_B'].widget.attrs.update({'class': 'fork_B hide_annoying_parent'})
        self.fields['fork_question_pt_B'].widget.attrs.update({'class': 'fork_B hide_annoying_parent'})
        self.fields['fork_question_es_B'].widget.attrs.update({'class': 'fork_B hide_annoying_parent'})

        self.fields['fork_speech_BB'].widget.attrs.update({'class': 'fork_B hide_annoying_parent'})

        self.fields['fork_question_en_C'].widget.attrs.update({'class': 'fork_C hide_annoying_parent'})
        self.fields['fork_question_pt_C'].widget.attrs.update({'class': 'fork_C hide_annoying_parent'})
        self.fields['fork_question_es_C'].widget.attrs.update({'class': 'fork_C hide_annoying_parent'})

        self.fields['fork_speech_CC'].widget.attrs.update({'class': 'fork_C hide_annoying_parent'})

        self.fields['fork_question_en_D'].widget.attrs.update({'class': 'fork_D hide_annoying_parent'})
        self.fields['fork_question_pt_D'].widget.attrs.update({'class': 'fork_D hide_annoying_parent'})
        self.fields['fork_question_es_D'].widget.attrs.update({'class': 'fork_D hide_annoying_parent'})

        self.fields['fork_speech_DD'].widget.attrs.update({'class': 'fork_D hide_annoying_parent'})

        self.fields['fork_question_en_E'].widget.attrs.update({'class': 'fork_E hide_annoying_parent'})
        self.fields['fork_question_pt_E'].widget.attrs.update({'class': 'fork_E hide_annoying_parent'})
        self.fields['fork_question_es_E'].widget.attrs.update({'class': 'fork_E hide_annoying_parent'})

        self.fields['fork_speech_EE'].widget.attrs.update({'class': 'fork_E hide_annoying_parent'})

        self.fields['fork_question_en_F'].widget.attrs.update({'class': 'fork_F hide_annoying_parent'})
        self.fields['fork_question_pt_F'].widget.attrs.update({'class': 'fork_F hide_annoying_parent'})
        self.fields['fork_question_es_F'].widget.attrs.update({'class': 'fork_F hide_annoying_parent'})

        self.fields['fork_speech_FF'].widget.attrs.update({'class': 'fork_F hide_annoying_parent'})
                                                 
        # hide_annoying_parent and Read Only 
        # tried and didn't work, will deal with it later.
        self.fields['conversation'].widget.attrs.update({'class': 'speech_conv hide_annoying_parent'})


def all_conv_view(request):

    all_conv = Conversation.objects.values_list('title', 'id', 'is_quest', 'quest_step')
    total_convs = len(all_conv)
    print(all_conv[0])


    #check if conversations are part of a quest? idk

    return render(request, 'site/all_conv.html', { "convs" : all_conv, "total_conv" : total_convs } )


def conversation_create_view(request):
    #form = ConversationCreateForm()

    if request.method == 'POST':        # if it is processing the form with a new conversation
        form = ConversationCreateForm(request.POST)
        if form.is_valid():
            new_form = form.save()
            request.session['conv_request'] = str(new_form.id)   # get the primary key of the new conversation

            return redirect("all_conv") # change to edit_conv.
            #redirect to a speech edit with the get method for x talk
    else:
        form = ConversationCreateForm()


    return render(request,'site/forms/create_conversation.html', {'form' : form })


def edit_conv_view(request,pk):
    print("")
    
    conv = Conversation.objects.get(id=pk)
    conv_name = f"{conv.title} Speech []"

    conv_form = ConversationEditForm(instance=conv)


    initial_values = {
        'conversation' : pk,
        'name' : conv_name,
        'txt_en' : "LOLOLOL" }

    speech_form = SpeechCreateForm(initial=initial_values)

    # This section will be updated with the HTMX stuff.
    # Maybe we leave this function to only get this.

    if request.method == 'POST':
        #remove instance, add initial? Careful with name order
        new_conv = ConversationEditForm(request.POST, instance=conv)
        if new_conv.is_valid():
            new_conv.save()

            conv_form = new_conv
            conv = Conversation.objects.get(id=pk)
            #you can also add old_conv to show a com a comparison

    # Get all speeches linked to this
    speeches = Speech.objects.filter(conversation=pk)


    context = {

        'pk' : pk,  #no need to be this way but i'm fed up
        
        'conv_form' : conv_form,
        'conv' : conv,
        #'old_conv' : old_conv

        'speech_form' : speech_form,

        'speeches' : speeches

    }
    return render(request,'site/forms/edit_conv.html', context)
# -----------------------------------------------------

# Create speech

class ForkCreateForm(ModelForm): 
    class Meta:
            model = Speech
            fields = [
                'fork_question_en_A',
                'fork_question_pt_A',
                'fork_question_es_A',
                
                'fork_question_en_B',
                'fork_question_pt_B',
                'fork_question_es_B',

                'fork_question_en_C',
                'fork_question_pt_C',
                'fork_question_es_C',

                'fork_question_en_D',
                'fork_question_pt_D',
                'fork_question_es_D',

                'fork_question_en_E',
                'fork_question_pt_E',
                'fork_question_es_E',

                'fork_question_en_F',
                'fork_question_pt_F',
                'fork_question_es_F',
                ]

def add_as_fork(og_speech,speech,conv):
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

def validate_speech(conv_pk,form,reply_to=None):
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

            while next_chain is not None:
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



def create_speech_process(request,pk): # saves speech
    # can be used to just edit too, just change the
    # htmx command to swap current field
    conv = get_object_or_404(Conversation,id=pk)

    if request.method == 'POST':
        form = SpeechCreateForm(request.POST)

        if form.is_valid():
            
            speech = form.save(commit=False) #we still want to alter the name
            
            speech.save()

            is_fork = False
            #speech.conversation = pk
            #add the conversation
            #alter the name
            
    return render(request,'site/htmx/single_speech.html', {'speech' : speech, 'is_fork' : is_fork }) # will be replaced with render



def edit_speech_process(request,speech_pk):
    # Gets form with said speech, adds all its values as default.
    print("")
    

def get_fork_fields(obj,language_group): # management of my own madness
    speech = obj

    match language_group:

        case "all":
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


def fork_question_process(request,speech_pk):
    print("Before pk test")
    # this register the fork
    speech = get_object_or_404(Speech,id=speech_pk)

    print("AFTER pk test")

    if request.method == 'POST':
        form = ForkCreateForm(request.POST, instance=speech)

        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print(" ")
        print( "ok so far?")
        if form.is_valid():

            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print( "Form was valid?")




            form.save()
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print(" ")
            print( "Form was saved?")

            msg = "the fork worked?"

            #speech.has_fork=True
            #speech.save() #they deal with the same object, but has_fork is not a field
            return render(request,'site/htmx/fork_speech_form.html', { 'speech' : speech, 'msg' : msg }) 
        else:
            print("the form is NOOOOOOOOOOOOOOOOOOOOOOT VALID \n\n\n")

def get_fork_question(request,speech_pk):
    # gets speech form where speech_pk is the one being replied to
    # This form is merely to use the fork fields.
    # The render once it is accepted immediately calls a branch_speech_process fork

    speech = get_object_or_404(Speech,id=speech_pk)
    

    if request.method == 'POST':

        my_initials = get_fork_fields(speech,"all")

        form = ForkCreateForm(instance=speech, initial=my_initials)

        # Preparing form fields data for template -------------------------------

        # I am very aware i could make lists inside lists, but i HATE the template
        # of django when it comes to loops so that is how it is going to bef or today

        en_forks= get_fork_fields(speech,'en')
        pt_forks= get_fork_fields(speech,'pt')
        es_forks= get_fork_fields(speech,'es')

        # en_empties=[] # template's for each loop will check if it will hide the field or not
        # pt_empties=[]
        # es_empties=[]
        # field_groups = [] # False is all fields are empty

        # en_all_false = True

        # for en, pt, es in zip(en_forks, pt_forks, es_forks):
        #     en_empties.append(True) if en is None else en_empties.append(False)
        #     pt_empties.append(True) if pt is None else pt_empties.append(False)
        #     es_empties.append(True) if es is None else es_empties.append(False)


        #     if (en is None) and (pt is None) and (es is None):
        #         field_groups.append(False) # false
        #     else:
        #         field_groups.append(True) # field is in use

        
        context = {
            'form' : form,

            'speech' : speech, # mostly for the speech id formation, pk was giving trouble

        }


        return render(request,'site/htmx/fork_speech_form.html', context) 

    

