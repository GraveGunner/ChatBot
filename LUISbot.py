from botbuilder.core import TurnContext, ActivityHandler, RecognizerResult, MessageFactory
from botbuilder.ai.luis import LuisApplication, LuisPredictionOptions, LuisRecognizer
from botbuilder.schema import ChannelAccount
from luis import Luis

class LUISBot(ActivityHandler):

    def __init__(self):

        luis_app = LuisApplication("85e56c2f-7ed4-4da1-b6ec-775b5090f3a8","346756f90f054396ab25f97c61dc13a4","https://westus.api.cognitive.microsoft.com/")
        luis_option = LuisPredictionOptions(include_all_intents=True, include_instance_data=True)
        self.LuisReg = LuisRecognizer(luis_app, luis_option, True)
       
    async def on_members_added_activity(self,members_added: ChannelAccount,turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
    
    
    async def on_message_activity(self, turn_context: TurnContext):
        luis_result = await self.LuisReg.recognize(turn_context) # Used to deserialize the activity using the LuisRecognizer 
        result = luis_result.properties["luisResult"]
        await turn_context.send_activity(f"Top Intent : {result.top_scoring_intent.intent}")
        if len(result.entities):
            for i in range(len(result.entities)):
                await turn_context.send_activity(f" Entity Name: {result.entities[i].entity}")
                await turn_context.send_activity(f" Entity Type : {result.entities[i].type}") 

