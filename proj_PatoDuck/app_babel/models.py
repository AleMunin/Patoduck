import uuid
from django.db import models

# Create your models here.
class Character (models.Model):
 

    name = models.CharField(max_length=250, unique=True)

    name_pt = models.CharField(max_length=250, unique=True, blank=True, null=True)
    name_es = models.CharField(max_length=250, unique=True, blank=True, null=True)
    
    # * Status of the NPC
    
    walkable = models.BooleanField(default=False)   # If the character is a single sprite, then it blocks certain actions
    in_game = models.BooleanField(default=False)   # if the character is in the build of the game or not

    # ! Database Data
    id = models.CharField(max_length=16, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
    
class Action(models.Model):
    ACTION_CHOICES = {
        "NO" : "None",
        
        # ? Walk

        "WF" : "Walk Forward",
        "WB" : "Walk Back",
        "WR" : "Walk Right",
        "WL" : "Walk Left",

        # ? Jump

        "JP" : "Jump Once",
        "JM" : "Jump Multiple Times",

        # ? Shake

        "SK" : "Shake Sideways",
        "SU" : "Shake Upwards",

        # ? Misc
        
        "SP" : "Spin",
        "CF" : "Confused"

        # ? Emoji

    }

    action = models.CharField(max_length=30, choices = ACTION_CHOICES, default="NO")
    
    # TODO: On validation, only walking ones can have distance.
    duration = models.PositiveIntegerField(default=0)
    distance = models.PositiveIntegerField(default=0)   # for walk ones, you can introduce the value here
    
class Location (models.Model):

    name = models.CharField(max_length=250,unique=True)    
    name_pt = models.CharField(max_length=250, unique=True, blank=True, null=True)
    name_es = models.CharField(max_length=250, unique=True, blank=True, null=True)
    
    # ? Data of the location
    
    indoors = models.BooleanField(default=False)
    description = models.TextField()

    # ! Data for the database

    id = models.CharField(max_length=16, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # if you ever need connections, just create self keys here

    def __str__(self):
        return str(self.name)
    
class Quest(models.Model):
    id = models.CharField(max_length=25, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    title = models.CharField(max_length=250, unique=True)
    title_pt = models.CharField(max_length=250, unique=True, null=True)
    title_es = models.CharField(max_length=250, unique=True, null=True)

    description = models.TextField()
    description_pt = models.TextField(null=True)
    description_es = models.TextField(null=True)
    
    # ? Data for users

    condition = models.TextField() # This is just a comment for the user
    
    number_of_steps = models.PositiveIntegerField(default=0) #number of conversations it has.

    # It is possible to add a foreign key of items you need for the quest

    def __str__(self):
        return str(self.title)
    
class Conversation(models.Model):

    title = models.CharField(max_length=250, unique=True)

    # ? Those two seve mostly the same purpose but condition is a "flag" for queries. Meanwhile description helps understand the positioning
    condition = models.TextField(blank=True, null=True)
    description = models.TextField(blank = True, null=True)

    #? user status
    is_quest = models.BooleanField(default=False)   # Practical delimiter
    is_cutscene = models.BooleanField(default=False)   # Signals if it requires more attention
    in_game = models.BooleanField(default=False)    # If it is already in the build or not.
    

    my_code = models.TextField(blank=True, null=True) # In case we need to wrap things in code. the text is added on a tag.


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
    
    # ! Database info
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    quest_step = models.PositiveIntegerField(default=0) # Number assigned when following a quest.
    # total_speeches = models.PositiveIntegerField(default=0) # Used for accounting for rogue speeches and raising flags, but past me told me it is more trouble than it is worth
    
    is_linear = models.BooleanField(default=True)   #Signals if it it is linear.

    
    creation = models.TimeField(auto_now_add=True)  # For data collection purposes
    #pt_translated_at = models.TimeField(auto_now_add=True) 

    
    # * Flags
    
    broken_chain = models.BooleanField(default=False) # Marked true when some error has happened between its speeches


    def __str__(self):
        return str(self.title)
    

class Speech(models.Model):

    # UPDATE this model:
    # is_rogue for lone speeches when errors and deletions happen.
    # is_fork should be useful.
    # Add a "Localized" checkbox, in case the translation isn't 1 to 1, so we can keep an eye on it.

    # ! Already was sketching a Materialized Path Tree, without knowing what it is, so might as well follow the example of this: https://www.youtube.com/watch?v=CRxjoklS8v0
    # * If that fails use MP_node

    
    # ! Database Info
    
    id = models.CharField(max_length=6, default=uuid.uuid4, unique=True, primary_key=True, editable=False) # ! The id is the smallest lineIDs on Yarn Spinner don't mention if a limit exists, probably don't


    is_first = models.BooleanField(default=False)   # easier to track
    has_fork = models.BooleanField(default=False)   # Signaler of all the other things bellow
    is_fork = models.BooleanField(default=False) # ! Note: If it is reply to a Fork, it is false.
    fork_letter = models.TextField(max_length=26,blank=True) #TODO: Automate this
    next_is_cycled = models.BooleanField(default=False)
        # quick status that avoids infinite loops
        # If the next_speech property is not a direct fork, but another speech for cycled dialogue
    
    
    # ? User info
    name = models.CharField(max_length=250, unique=True) # TODO: Automate the generation of this, with AA, ABA, so on.
    comment = models.TextField(blank=True, null=True)    # Context, if needed.
    my_code = models.TextField(blank=True, null=True) # code, tags, so on


    # Every speech is part of a conversation
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.PROTECT
    )

    # Add your languages here, ironically the simplest part

    txt_en = models.TextField()
    txt_pt = models.TextField(blank=True, null = True)
    txt_es = models.TextField(blank=True, null = True)
    
    my_fork_question_en = models.TextField(blank=True, null = True) # TODO: Enforce validation of this if it is a fork.abs
    my_fork_question_pt = models.TextField(blank=True, null = True) # TODO: Enforce requirement of this if it is being translated
    my_fork_question_es = models.TextField(blank=True, null = True) # TODO: Enforce requirement of this if it is being translated


    # ! Flags 
    
    localized_pt = models.BooleanField(default=False)   # If it is not a literal translation. For whatever reason.
    localized_es = models.BooleanField(default=False)

    #proofread_en = models.BooleanField(default=False)
    #proofread_pt = models.BooleanField(default=False)
    #proofread_es = models.BooleanField(default=False)

    speaker = models.ForeignKey(    # NPC that says it
        Character,
        blank = True,
        null=True,
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

    # TODO: Remove action altogether and make it a field in here. There is no purpose    
    # act  = models.ForeignKey(Action,blank=True,null=True,related_name='action',on_delete= models.PROTECT)
    # action_moment = models.BooleanField(default=False) # ? False = Before, True = After the text is played.

    # -------------------------------------------

    previous_speech = models.ForeignKey(    # Make the register make sure this is empty if it is marked as first.clea
        'self',
        blank = True,
        null=True,
        related_name="speech_prev",
        on_delete = models.PROTECT
    )

    next_speech = models.ForeignKey( # ! Only if has_fork is false
        'self',
        blank = True,
        null=True,
        related_name="speech_next",
        on_delete = models.PROTECT
    )

    # ============================

    def __str__(self):
        return str(self.name)