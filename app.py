from flask import Flask, request, Response
from botbuilder.schema import Activity
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
import asyncio
from LUISbot import LUISBot

app = Flask(__name__)

loop = asyncio.get_event_loop()

botadaptersettings = BotFrameworkAdapterSettings("","")
botadapter = BotFrameworkAdapter(botadaptersettings)

luis = LUISBot()

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        jsonmessage = request.json
    else:
        return Response(status=415)
   
    activity = Activity().deserialize(jsonmessage)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""


    async def turn_call(turn_context: TurnContext):
        await luis.on_turn(turn_context)
    
    task = loop.create_task(botadapter.process_activity(activity, auth_header, turn_call))
    loop.run_until_complete(task)
    return("Done!")

if __name__ == "__main__":
    app.run("localhost", 4000)
 