import uuid # general library
from django.db import models # django libraries

# Create your models here.
class Character (models.Model):
 

    name = models.CharField(max_length=250, unique=True)

    name_pt = models.CharField(max_length=250, unique=True, blank=True, null=True)
    name_es = models.CharField(max_length=250, unique=True, blank=True, null=True)
    
    # * Status of the NPC
    
    walkable = models.BooleanField(default=False)   # If the character is a single sprite, then it blocks certain actions
    in_game = models.BooleanField(default=False)   # if the character is in the build of the game or not

    # ! Database Data
    id = models.CharField(max_length=4, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

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

    id = models.CharField(max_length=5, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # if you ever need connections, just create self keys here

    def __str__(self):
        return str(self.name)

class Stage (models.Model):
    ...
    # name
    # just helps categorize things on quest and conversation
    # so it is easier to sort conditional speeches
    

class Quest(models.Model):
    id = models.CharField(max_length=5, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    title = models.CharField(max_length=250, unique=True)
    title_pt = models.CharField(max_length=250, unique=True, null=True, blank=True)
    title_es = models.CharField(max_length=250, unique=True, null=True, blank=True)

    #? won't use this yet, but leaving here in case we do
    description = models.TextField()
    description_pt = models.TextField(null=True,blank=True)
    description_es = models.TextField(null=True,blank=True)
    
    # ? Data for users

    condition = models.TextField(blank=True) # This is just a comment for the user
    
    #todo: comment that out
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
    is_quest = models.BooleanField(default=False)   # redundant, but Practical delimiter
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
    id = models.CharField(max_length=8, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    quest_step = models.PositiveIntegerField(default=0) # Number assigned when following a quest.
    # total_speeches = models.PositiveIntegerField(default=0) # Used for accounting for rogue speeches and raising flags, but past me told me it is more trouble than it is worth
    
    is_linear = models.BooleanField(default=True)   #Signals if it it is linear.

    
    creation = models.TimeField(auto_now_add=True)  # For data collection purposes
    #pt_translated_at = models.TimeField(auto_now_add=True) 

    
    # * Flags
    
    broken_chain = models.BooleanField(default=False) # Marked true when some error has happened between its speeches


    def __str__(self):
        return str(self.title)
    
class Conditional(models.Model):
    
    id = models.CharField(max_length=4, default=uuid.uuid4, unique=True, primary_key=True, editable=False,)
    name = models.CharField(max_length=250, unique=False, null=True)
    
    comment = models.CharField(max_length=250, unique=False, null=True)
    
    double_else = models.BooleanField(default=False) #? Flag for validation error
    
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.PROTECT,
        related_name="conditionals"
    )

    
class Speech(models.Model):

    # ! Database Info
    
    id = models.CharField(max_length=6, default=uuid.uuid4, unique=True, primary_key=True, editable=False,) # ! The id is the smallest lineIDs on Yarn Spinner don't mention if a limit exists, probably don't

    # ? Major content
    
    txt_en = models.TextField()
    txt_pt = models.TextField(blank=True, null = True)
    txt_es = models.TextField(blank=True, null = True)
    
    #? Fork questions, only show up if they're forks
    
    fq_en = models.TextField(blank=True, null = True)
    fq_pt = models.TextField(blank=True, null = True)
    fq_es = models.TextField(blank=True, null = True)
    
    
    
    name = models.CharField(max_length=250, unique=False, null=True)
    
    #? Every speech is part of a conversation
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.PROTECT,
        related_name="speeches"
    )
    
    previous_speech = models.ForeignKey(    # Make the register make sure this is empty if it is marked as first.clea
        'self',
        blank = True,
        null=True,
        related_name="replies",
        on_delete = models.PROTECT
    )


    #! Avoid validation and loops through this
    #! Give preference for this only to be cycled responses
    
    next_speech = models.ForeignKey(
        'self',
        blank = True,
        null=True,
        related_name="merges_back",
        on_delete = models.PROTECT
    )
    
    conditional = models.ForeignKey(
        Conditional,
        blank = True,
        null=True,
        related_name="ifs",
        on_delete = models.PROTECT
    )
    
    
    
    
    #? Speaker
    #! related_name = speaks
    
    #? Portrait


    #? Status and flags -------------------------
    
    is_first = models.BooleanField(default=False)   # easier to track
    
    has_fork = models.BooleanField(default=False)
    is_fork = models.BooleanField(default=False)
    next_is_cycled = models.BooleanField(default=False) 
    
    #todo is_cycled = models.BooleanField(default=False) 
    #todo is_conditional = models.BooleanField(default=False)
    #? Localized PT
    #? Localized ES
    
    #? Proofread EN
    #? Proofread PT
    #? Proofread ES

    def __str__(self):
        return str(self.name)