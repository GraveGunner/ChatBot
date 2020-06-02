from botbuilder.core import TurnContext, ActivityHandler, RecognizerResult, MessageFactory
from botbuilder.ai.luis import LuisApplication, LuisPredictionOptions, LuisRecognizer
from botbuilder.schema import ChannelAccount
import Database as db
from Database import cursor
from random import randint
class LUISBot(ActivityHandler):

    def __init__(self):

        luis_app = LuisApplication("85e56c2f-7ed4-4da1-b6ec-775b5090f3a8","346756f90f054396ab25f97c61dc13a4","https://westus.api.cognitive.microsoft.com/")
        luis_option = LuisPredictionOptions(include_all_intents=True, include_instance_data=True)
        self.LuisReg = LuisRecognizer(luis_app, luis_option, True)
        self.greet = ['Hey', 'Hello', 'Hi', 'Hello, how may I help you?', 'Welcome to ChatBot', 'Good Day']
       
    async def on_members_added_activity(self,members_added: ChannelAccount,turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
    
    
    async def on_message_activity(self, turn_context: TurnContext):
        luis_result = await self.LuisReg.recognize(turn_context) # Used to deserialize the activity using the LuisRecognizer 
        result = luis_result.properties["luisResult"]
        if result.top_scoring_intent.intent == 'Pizza Order':
            topping = None 
            size = None
            for i in range(len(result.entities)):
                if topping == None and result.entities[i].type == 'Topping':
                    topping = result.entities[i].entity
            if topping == None:
                await turn_context.send_activity("Please enter with topping specification")
            for i in range(len(result.entities)):
                if size == None and result.entities[i].type == 'Size':
                    size = result.entities[i].entity
            if size == None:
                await turn_context.send_activity("Please enter with size specification")
            if topping != None and size != None:           
                await turn_context.send_activity(f"Total Price is {db.pizzaorder(topping, size)} INR")
        if result.top_scoring_intent.intent == 'Greeting':
            await turn_context.send_activity(f"{self.greet[randint(0, len(self.greet))]}")
        # await turn_context.send_activity(f"Top Intent : {result.top_scoring_intent.intent}")
        # if len(result.entities):
        #     for i in range(len(result.entities)):
        #         await turn_context.send_activity(f" Entity Name: {result.entities[i].entity}")
        #         await turn_context.send_activity(f" Entity Type : {result.entities[i].type}") 

