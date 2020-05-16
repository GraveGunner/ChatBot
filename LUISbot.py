from botbuilder.core import TurnContext, ActivityHandler, RecognizerResult, MessageFactory
from botbuilder.ai.luis import LuisApplication, LuisPredictionOptions, LuisRecognizer
from botbuilder.schema import ChannelAccount
from luis import Luis

class LUISBot(ActivityHandler):

    def __init__(self):
        # luis_app = LuisApplication("85e56c2f-7ed4-4da1-b6ec-775b5090f3a8","346756f90f054396ab25f97c61dc13a4","https://westus.api.cognitive.microsoft.com/luis/api/v2.0/")
        # luis_option = LuisPredictionOptions(include_all_intents=True, include_instance_data=True)
        # self.LuisReg = LuisRecognizer(luis_app, luis_option, True)
        self.luis_model =  Luis("https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/85e56c2f-7ed4-4da1-b6ec-775b5090f3a8?verbose=true&timezoneOffset=0&subscription-key=346756f90f054396ab25f97c61dc13a4&q=")

    async def on_members_added_activity(self,members_added: ChannelAccount,turn_context: TurnContext):
        for member_added in members_added:
            await turn_context.send_activity("Hello and welcome!")
    
    
    async def on_message_activity(self, turn_context: TurnContext):
        msg = turn_context.activity.text
        await turn_context.send_activity(f"You said {msg}")
        analysis =self.luis_model.analyze(msg)
        intent = analysis.best_intent()
        # luis_result = await self.LuisReg.recognize(msg)
        # intent = LuisRecognizer.top_intent(luis_result)
        await turn_context.send_activity(f"Top Intent : {intent.intent}")
        # result = luis_result.properties["luisResult"]
        # await turn_context.send_activity(f" Luis Result {result.entities[0]}") 