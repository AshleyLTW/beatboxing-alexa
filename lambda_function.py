#------------------------------Part1--------------------------------
# In this part we define a list that contains the player names, and 
# a dictionary with player biographies
sound_list = ["Bass Drum"]

first_choice_list = ["rhythm", "sound", "rhythms", 'sounds']

sound_explanation = {"Bass Drum": "Boots"}
#------------------------------Part2--------------------------------
# Here we define our Lambda function and configure what it does when 
# an event with a Launch, Intent and Session End Requests are sent. # The Lambda function responses to an event carrying a particular 
# Request are handled by functions such as on_launch(event) and 
# intent_scheme(event).
def lambda_handler(event, context):
    if event['session']['new']:
        on_start()
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event)
    elif event['request']['type'] == "IntentRequest":
        return intent_scheme(event)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_end()
#------------------------------Part3--------------------------------
# Here we define the Request handler functions
def on_start():
    print("Session Started.")

def on_launch(event):
    onlaunch_MSG = "Hi, welcome to Boots and Cats Beatbox. Do you want to learn new sounds or new rhythms today?"
    reprompt_MSG = "Do you want to learn sounds or rhythms?"
    card_TEXT = "Sounds or Rhythms?"
    card_TITLE = "Sounds or Rhythms?"
    return output_json_builder_with_reprompt_and_card(onlaunch_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def on_end():
    print("Session Ended.")
#-----------------------------Part3.1-------------------------------
# The intent_scheme(event) function handles the Intent Request. 
# Since we have a few different intents in our skill, we need to 
# configure what this function will do upon receiving a particular 
# intent. This can be done by introducing the functions which handle 
# each of the intents.
def intent_scheme(event):
    
    intent_name = event['request']['intent']['name']

    if intent_name == "goto_sounds_menu":
        return rhythm_or_sound(event)        
    elif intent_name in ["AMAZON.NoIntent", "AMAZON.StopIntent", "AMAZON.CancelIntent"]:
        return stop_the_skill(event)
    elif intent_name == "AMAZON.HelpIntent":
        return assistance(event)
    elif intent_name == "AMAZON.FallbackIntent":
        return fallback_call(event)
#---------------------------Part3.1.1-------------------------------
# Here we define the intent handler functions
def rhythm_or_sound(event):
    bb_type = event['request']['intent']['slots']['first_choice']['value']
    first_choice_lower=[w.lower() for w in first_choice_list]
    lower_bbt = bb_type.lower()
    if lower_bbt in first_choice_lower:
        reprompt_MSG = "Sounds or Rhythms?"
        card_TEXT = "You've picked " + lower_bbt
        card_TITLE = "You've picked " + lower_bbt
        
        if (lower_bbt == 'sounds') or (lower_bbt == 'sound'):
            return sound_selector(event)  
        
        return output_json_builder_with_reprompt_and_card(lower_bbt, card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        wrongname_MSG = "Sounds or Rhythms?"
        reprompt_MSG = "Sounds or Rhythms?"
        card_TEXT = "Use the full name."
        card_TITLE = "Wrong name."
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
        
        
def sound_selector(event):
    sound_type = event['request']['intent']['slots']['sounds']['value']
    sound_lower = [w.lower() for w in sound_list]
    lower_sound = sound_type.lower()
    if lower_sound in sound_lower:
        reprompt_MSG = "You can learn these sounds:" + ', '.join(map(str, sound_list)) + "Which sound would you like to learn?"
        card_TEXT = "Time to learn the " + lower_sound
        card_TITLE = "Time to learn the " + lower_sound
        
        return output_json_builder_with_reprompt_and_card(lower_bbt, card_TEXT, card_TITLE, reprompt_MSG, False)
    else:
        wrongname_MSG = "You haven't used the full name of a player. If you have forgotten which players you can pick say Help."
        reprompt_MSG = "Do you want to hear more about a particular player?"
        card_TEXT = "Use the full name."
        card_TITLE = "Wrong name."
        return output_json_builder_with_reprompt_and_card(wrongname_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)    
    
def stop_the_skill(event):
    stop_MSG = "Thank you. Bye!"
    reprompt_MSG = ""
    card_TEXT = "Bye."
    card_TITLE = "Bye Bye."
    return output_json_builder_with_reprompt_and_card(stop_MSG, card_TEXT, card_TITLE, reprompt_MSG, True)
    
def assistance(event):
    assistance_MSG = "You can choose among these players: " + ', '.join(map(str, sound_list)) + ". Be sure to use the full name when asking about the player."
    reprompt_MSG = "Do you want to hear more about a particular player?"
    card_TEXT = "You've asked for help."
    card_TITLE = "Help"
    return output_json_builder_with_reprompt_and_card(assistance_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)

def fallback_call(event):
    fallback_MSG = "I can't help you with that, try rephrasing the question or ask for help by saying HELP."
    reprompt_MSG = "Do you want to hear more about a particular player?"
    card_TEXT = "You've asked a wrong question."
    card_TITLE = "Wrong question."
    return output_json_builder_with_reprompt_and_card(fallback_MSG, card_TEXT, card_TITLE, reprompt_MSG, False)
#------------------------------Part4--------------------------------
# The response of our Lambda function should be in a json format. 
# That is why in this part of the code we define the functions which 
# will build the response in the requested format. These functions
# are used by both the intent handlers and the request handlers to 
# build the output.
def plain_text_builder(text_body):
    text_dict = {}
    text_dict['type'] = 'PlainText'
    text_dict['text'] = text_body
    return text_dict

def reprompt_builder(repr_text):
    reprompt_dict = {}
    reprompt_dict['outputSpeech'] = plain_text_builder(repr_text)
    return reprompt_dict
    
def card_builder(c_text, c_title):
    card_dict = {}
    card_dict['type'] = "Simple"
    card_dict['title'] = c_title
    card_dict['content'] = c_text
    return card_dict    

def response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    speech_dict = {}
    speech_dict['outputSpeech'] = plain_text_builder(outputSpeach_text)
    speech_dict['card'] = card_builder(card_text, card_title)
    speech_dict['reprompt'] = reprompt_builder(reprompt_text)
    speech_dict['shouldEndSession'] = value
    return speech_dict

def output_json_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value):
    response_dict = {}
    response_dict['version'] = '1.0'
    response_dict['response'] = response_field_builder_with_reprompt_and_card(outputSpeach_text, card_text, card_title, reprompt_text, value)
    return response_dict
