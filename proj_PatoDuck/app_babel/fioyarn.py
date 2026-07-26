
#? The classes on this tool can respond to a json translation or directly from database
#? The idea is that you can use this script alone to convert json files or the database directly
# TODO: While I get the logic this relied way too much on json, you might want to just rewrite it with it as refernece

import pprint
from .models import * #! remove this on single script
PRIMARY_LANG = "en" # This is an identifier

CROCHET_VERSION = "#__PrivCrochet_version:1"
PATODUCK = "#__PatoDuckParsed"


BEGIN = "---"
END_NODE = "==="


class Dialogue():
    """
    This object collects input from json or Speech objects.
    A Story class will iterate through its list, and orders it to format itself.
    """
    
    def __init__(self, data):
        """
        ? data is essentially the same as the fields on the database from a Speech object
        
        """
        #! temporary:
        
        self.speaker = "Tester"
        
        # self.forks_en = [ #! fake data test
        #     ("fork_name A", "fork_hash_A", "fork_question A"),
        #     ("fork_name B", "fork_hash_B", "fork_question B"),
        #     ("fork_name C", "fork_hash_C", "fork_question C"),
        # ]
        
        def dj_get_my_forks(self):
            #? relies on data being a Speech object
            # ! Speech obj has changed since this was made
            for fork in Speech.objects.filter(previous_speech=data):
                
                f_en = (fork.name, fork.id, fork.fq_en)
                f_pt = (fork.name, fork.id, fork.fq_en)
                f_es = (fork.name, fork.id, fork.fq_es)
                
                #? add formating here if you must
                
                self.forks_en.append(f_en)
                #self.fork_pt.append(f_pt)
                #self.fork_es.append(f_es)
        
        #----
        
        self.group = None # This will basically become my_code
        self.my_space = 0 # Given by Story
        
        #! removed: fork_letter, conversation ID
        
        #? Data from Speech  ------------------------------------------------
        
        for key, value in vars(data).items():
            setattr(self, key, value)
        

        # pprint.pprint(vars(self))
        #! for testing sake
        
        if self.has_fork:
            dj_get_my_forks(self)
            print(self.forks_en)
        print(f"\033[94m Dialogue [{self.name}] was created \033[0m")
        
        
    #? Dialogue Methods --------------------------------------------------------------    


    def l(self):    #stands for line_hash
        return f"   #line:{self.id}" #former line_hash
    

    # def get_group(self, group):
    #     self.group = group

    # def get_my_space(self,space):   # gets base space
    #     self.my_space = 0
        
    # def nested_spaces(self, text,nest_num=1): # I do not intend to make many nestings, but i don't want to handle cases individually.
    #     space = f"   "
    #     i = 0
    #     while i < (nest_num+self.my_space):
    #         space = space + space
    #         i +=1
    #     return space + text
    
    
    # def option(self,text):
    #     text = f"->{text}{self.l()}"
    #     text = self.nested_spaces(text,1)   # it needs at least 1 space.
    #     return text

    def speech(self,lang=PRIMARY_LANG,space=False): #formats the speech, and only the speech. #! No options, no nesting.

        match lang:
            case "en":
                speech = f"{self.speaker}:{self.txt_en}{self.l()}"
            case "es":
                speech = f"{self.speaker_es}:{self.txt_es}{self.l()}"
            case "pt":
                speech = f"{self.speaker_pt}:{self.txt_pt}{self.l()}"
 
        # if space is True: #todo: add later
        #     self.nested_spaces(speech)
        return speech
    
    # def jump(self, nxt=None): 
    #     #Next is either empty (the dialogue is linear) or it carries the fork name
    #     if nxt is None:    #if is linear
    #         node = self.next_speech_id # will print the name
    #         return self.nested_spaces(f"<<jump {node}>>\n")
    #     else:
    #         return self.nested_spaces(f"<<jump {nxt}>>\n")    #all options require at least one nested space.

    def fork(self,lang=PRIMARY_LANG):
        options = ""
        space = "    " #? exact space from the yarnspinner documentation
        #! for other languages, add here before looping
        
        if self.has_fork:
            options="\n"
            for f_name, f_hash, f_question in self.forks_en:
                #todo: be based on language
                #todo: add the hash
            
                options += f"-> {f_question}  #line:{f_hash} \n{space}<<jump {f_name}>>\n"
        
        
        #print(f"----------- \n returning: \n {options} \n")
        return options

       
    def header(self):
        
        name = f"title: {self.name}\n"
        if self.group:
            group = f"group: {self.group}\n"
        else:
            group = ""

        head = f"{name}{group}{BEGIN}\n"

        return head #hihihi

    def boder(self, lang=PRIMARY_LANG): # returns the body, #! for one language.

        # you can make a comment variable and mention the previous speech

        speech = self.speech(lang)

        # # #iterates options
        if (fork_string := self.fork(lang)):
            body = f"{speech}\n{fork_string}"
        else:
            # if self.next_speech_id is not None:
            # jump = self.jump()

            jump = "<< jump test to be replaced >>" #! remove here

            body = f"{speech} \n{jump}"

        return body #huh...
    
    

    # #? Major interaction ----------------------------------


    def send_nodes(self,lang=PRIMARY_LANG, test=True):
        head = self.header()
        body = self.boder(lang)
        node = f"{head}{body}\n{END_NODE}"
        
        # if test:
        #     print(node)
        return node

    
    
    
    

class Story():
    """
    This object is responsible for the .yarn file itself.
    """
    ...
    def __init__(self, data):
        
        # Major loop properties
        
        self.dialogues = [] # a list of Dialogue objects to iterate

        # metadata -----------------------------

        self.initial_x = 160
        self.initial_y = 210

        self.path = None
        self.print_step = 0 # not needed, made it local
        self.nest_step = 0  # Just in case, for if statements

        
        # content based on language 
        self.nodes = {
            "en" : "",
            "pt" : "",
            "es" : "",
        }
        
        # flags

        self.translated_pt = False  #compares the forks and hashes and if they ALL have content, will make localization fles.
        self.translated_es = False


        for key, value in vars(data).items():
            setattr(self, key, value)
            #pprint.pprint(data)
        
        #pprint.pprint(vars(self))
        
        
    #? INTERNAL METHODS ====================================
    
    # def find_my_path():
    #     ...
    #     #! make django pick a path too
         
    def first_header(self, lang=PRIMARY_LANG):
        
        #todo: Make actual language headers

        content = f"PatoDuck Version: 0.2 \n{CROCHET_VERSION}\n\n\n"
        # add comments and other datas here

        return content
    
    
    # #? EXTERNAL COMMUNICATION ==============================
    
    def collect(self, obj):
        #? It collects the object, content come only on printing file
        if isinstance(obj,Dialogue):
            self.dialogues.append(obj)
            print(f"\033[94m Dialogue [{obj.name}] was collected \033[0m")
            
        else:
            print("!!!! Error: collected data is not Dialogue")
    
    def spin_it(self,   lang=PRIMARY_LANG,  filing=False):
        """
        This method builds the content of the .yarn file
        pathing variable determines if 
        """
        # Set up ------------------------
        if filing:
            self.find_my_path() #! Path will change if independent or in Django
        
        content = []
        content.append(self.first_header())
        print_step = 0
        
        # --------------------------
        
        for dialogue in self.dialogues:
            #TODO might add later:
            #dialogue.get_my_space(print_step) #? Nesting
            #dialogue.get_group(group) #? grouping
            
            content.append(dialogue.send_nodes())
        
        for node in content:
            print(node)
            
    #     with open(self.path,'w') as my_yarn:
    #         #? pay attention to this part when you need
    #         #? code between header and dialogues
            
    #         for node in content:
    #             my_yarn.write(node)
            
    #     print(f"File created at {self.path}")
    
    # #? Testing --------------------------------
    
    # def test_dialogue(self,lang=PRIMARY_LANG):
    #     print("\nDumping dialogue for testing:")
    #     for dialogue in self.dialogues:
    #         print (f"{dialogue.test_node()} \n\n")
        

    
#? Functions -------------------------------------------------------


def is_speech(data):
    fields = fields = [
        "_state",
        "comment",
        "conversation_id",
        "has_fork",
        "id",
        "is_first",
        "is_fork",
        "line_hash", #! Might not need
        "localized_es",
        "localized_pt", 
        "name",
        "next_speech_id", #! Might not need
        "portrait",
        "previous_speech_id", #! Might not need
        "speaker_id",
        "txt_en",
        "txt_es",
        "txt_pt",
    ]
    
    for field in fields:
        if field not in data:
            print(" \n\n!!!!!!!!!!!!!!!!!!!!!!!!")
            print(f"The field \"{field}\" is missing on this speech")
            print("!!!!!!!!!!!!!!!!!!!!!!!! \n\n")
            return False
    
    return True

