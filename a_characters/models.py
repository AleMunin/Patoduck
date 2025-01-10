from django.db import models
import uuid

# -----------------------------------------------------------------------

class Character (models.Model):

    # add creation date  (actualy make another table with that)

    name = models.CharField(max_length=250, unique=True)
    name_pt = models.CharField(max_length=250, unique=True, blank=True, null=True)
    name_es = models.CharField(max_length=250, unique=True, blank=True, null=True)

    walkable = models.BooleanField(default=False)   # If the character is a single sprite, then it blocks certain actions

    published= models.BooleanField(default=False)
    portraits= models.SmallIntegerField(default=0)

    # Description?


    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

class Action(models.Model):
    ACTION_CHOICES = {
        "NO" : "None",

        "WF" : "Walk Forward",
        "WB" : "Walk Back",
        "WR" : "Walk Right",
        "WL" : "Walk Left",

        "JP" : "Jump Once",
        "JM" : "Jump Multiple Times",

        "SK" : "Shake Sideways",
        "SU" : "Shake Upwards",

        "SP" : "Spin",


    }

    action = models.CharField(max_length=30, choices = ACTION_CHOICES, default="NO")

    duration = models.PositiveIntegerField(default=0)
    distance = models.PositiveIntegerField(default=0)

class Location (models.Model):

    name = models.CharField(max_length=250,unique=True)
    
    indoors = models.BooleanField(default=False)
    #Inside of self foreign key?

    description = models.TextField()

    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # if you ever need connections, just create self keys here

    def __str__(self):
        return str(self.name)


class Quest(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    title = models.CharField(max_length=250, unique=True)

    title_pt = models.CharField(max_length=250, unique=True, null=True)
    title_es = models.CharField(max_length=250, unique=True, null=True)

    condition = models.TextField()

    description = models.TextField()
    description_pt = models.TextField(null=True)
    description_es = models.TextField(null=True)

    number_of_steps = models.PositiveIntegerField(default=0) #number of conversations it has.

    # It is possible to add a foreign key of items you need for the quest

    def __str__(self):
        return str(self.title)


class Conversation(models.Model):

    title = models.CharField(max_length=250, unique=True)

    condition = models.TextField(blank=True, null=True)    # Just a forewarning to implementing the quest
    description = models.TextField()        # Context

    creation = models.TimeField(auto_now_add=True)  # For data collection purposes
    #pt_translated_at = models.TimeField(auto_now_add=True) 

    is_quest = models.BooleanField(default=False)   # Practical delimiter
    is_cutscene = models.BooleanField(default=False)   # Signals if it requires more attention
    is_linear = models.BooleanField(default=True)   #Signals if it it is linear.

    quest_step = models.PositiveIntegerField(default=0) #useful to order several quests.
    total_speeches = models.PositiveIntegerField(default=0) #counter of quests
    broken_chain = models.BooleanField(default=False)

    my_code = models.TextField(blank=True, null=True)


    location = models.ForeignKey(   # No need to have it, it is more useful if it is part of a quest, or cutscene
        Location,
        blank = True,
        null=True,
        on_delete=models.PROTECT
    )

    quest = models.ForeignKey(  # If quest step > 1 it HAS to have a quest indexed. Remember this on the forms
        Quest,
        blank = True,
        null=True,
        on_delete=models.PROTECT
    )

    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.title)

class Speech(models.Model):

    # UPDATE this model:
    # is_rogue for lone speeches when errors and deletions happen.
    # is_fork should be useful.
    # Add a "Localized" checkbox, in case the translation isn't 1 to 1, so we can keep an eye on it.

    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    line_hash = models.CharField(max_length=6, blank=True, null=True, unique=True) #yarn annoyances

    
    comment = models.TextField(blank=True, null=True)    # Context, could have been label, but fuck it.
    my_code = models.TextField(blank=True, null=True)

    name = models.CharField(max_length=250, unique=True) #"This needs to be a title for speech to go on the .yarn export" # maybe create a function to automate it

    # Every speech is part of a conversation
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.PROTECT
    )

    # Add your languages here

    txt_en = models.TextField()
    txt_pt = models.TextField(blank=True, null = True)
    txt_es = models.TextField(blank=True, null = True)

    localized_pt = models.BooleanField(default=False)   # If it is not a literal translation. For whatever reason.
    localized_es = models.BooleanField(default=False)

    #proofread_en = models.BooleanField(default=False)
    #proofread_pt = models.BooleanField(default=False)
    #proofread_es = models.BooleanField(default=False)

    speaker = models.ForeignKey(    # NPC that says it
        Character,
        on_delete = models.PROTECT
    )

    CHOICES_EMOTION = { # I really don't see the point in doing key-relationship thing in here, but everyone is doing and
                        # like the masses I can't be bothered by critical thinking, especially if it will lead me to a bug

        'DF' : "Default",
        'CT' : "Custom",
        
        'HP' : "Happy",
        'SD' : "Sad",

        "EX" : "Excited",
        "TD" : "Tired",

        "TD" : "Thoughtful / Thinking",
        "DT" : "Distracted",

        'TN' : "Tense",
        'PN' : "In Pain",

        'CF' : "Confused",
        'DZ' : "Dizzy",

        'CR' : "Crying",
        'TR' : "Teary",
        'IP' : "Inpired /Amazed",

        'SP' : "Surprised",
        "WR" : "Worried",
    }

    portrait = models.CharField(
        max_length = 25, #because who knows, i hate the initials
        choices = CHOICES_EMOTION,
        default="DF"
    )

    # -------------------------------------------

    is_first = models.BooleanField(default=False)   # easier to track
    is_fork = models.BooleanField(default=False) # WAY easier to track. If it is reply to a Fork, it is false.
    #fork_letter = models.CharField(max_length = 16, null=True, blank=True)
    fork_letter = models.TextField(max_length=15,blank=True, null=True)

    previous_speech = models.ForeignKey(    # Make the register make sure this is empty if it is marked as first.
        'self',
        blank = True,
        null=True,
        related_name="speech_prev",
        on_delete = models.PROTECT
    )

    next_speech = models.ForeignKey(
        'self',
        blank = True,
        null=True,
        related_name="speech_next",
        on_delete = models.PROTECT
    )

    # --------------------------------------

    has_fork = models.BooleanField(default=False)   # Signaler that the rest here exists

    

    # Django wants the field to be directly related to a variable.
    # In my innocence i tried to put this on a list and it acted like a girl from tinder

    fork_question_en_A = models.TextField(blank = True, null = True)
    fork_question_pt_A = models.TextField(blank = True, null = True)
    fork_question_es_A = models.TextField(blank = True, null = True)

    fork_speech_AA = models.ForeignKey(  # link to the speech that is a fork
                'self',
                blank = True,
                null=True,
                related_name="fork_next_speech_A",
                on_delete = models.PROTECT
            )
    

    # ============================

    fork_question_en_B = models.TextField(blank = True, null = True)
    fork_question_pt_B = models.TextField(blank = True, null = True)
    fork_question_es_B = models.TextField(blank = True, null = True)

    fork_speech_BB = models.ForeignKey(  # link to the speech that is a fork
                'self',
                blank = True,
                null=True,
                related_name="fork_next_speech_B",
                on_delete = models.PROTECT
            )
    
    

    # ============================

    fork_question_en_C = models.TextField(blank = True, null = True)
    fork_question_pt_C = models.TextField(blank = True, null = True)
    fork_question_es_C = models.TextField(blank = True, null = True)

    fork_speech_CC = models.ForeignKey(  # link to the speech that is a fork
                'self',
                blank = True,
                null=True,
                related_name="fork_next_speech_C",
                on_delete = models.PROTECT
            )
    
    

    # ============================

    fork_question_en_D = models.TextField(blank = True, null = True)
    fork_question_pt_D = models.TextField(blank = True, null = True)
    fork_question_es_D = models.TextField(blank = True, null = True)

    fork_speech_DD = models.ForeignKey(  # link to the speech that is a fork
                'self',
                blank = True,
                null=True,
                related_name="fork_next_speech_D",
                on_delete = models.PROTECT
            )
    

    # ============================

    fork_question_en_E = models.TextField(blank = True, null = True)
    fork_question_pt_E = models.TextField(blank = True, null = True)
    fork_question_es_E = models.TextField(blank = True, null = True)

    fork_speech_EE = models.ForeignKey(  # link to the speech that is a fork
                'self',
                blank = True,
                null=True,
                related_name="fork_next_speech_E",
                on_delete = models.PROTECT
            )
    
    

    # ============================

    fork_question_en_F = models.TextField(blank = True, null = True)
    fork_question_pt_F = models.TextField(blank = True, null = True)
    fork_question_es_F = models.TextField(blank = True, null = True)

    fork_speech_FF = models.ForeignKey(  # link to the speech that is a fork
                'self',
                blank = True,
                null=True,
                related_name="fork_next_speech_F",
                on_delete = models.PROTECT
            )
    
    

    # ============================

    def __str__(self):
        return str(self.name)