#
# Usage: python callAPI.py PROMPTFILE TOOLFILE MAXMESSAGELENGTH
#
import pickle
import json
import sys
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from time import gmtime, strftime
import datetime
import os

GPT_MODEL = "gpt-4o"
client = OpenAI()

def parse_int(s, default=0):
    try:
        return int(s)
    except ValueError:
        return default

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


instance_id = "k1"
chat_start_time = datetime.datetime.now()

with open(sys.argv[1], "r") as promptfile:
    prompt = promptfile.read()

with open(sys.argv[2], 'r') as toolsfile:
    tools = json.load(toolsfile)

messages = []
messages.append({"role": "system", "content": "Instance -" + instance_id + "- created at " + str(chat_start_time)})
messages.append({"role": "system", "content": prompt})
print(messages[0]["role"])
print(messages[0]["content"])
print("")
yetread = 0

max_conversation_length = parse_int(sys.argv[3], 20)


isActive = True
isError = False
isCallRep = False

message_pickle_location = "chat_history/" + instance_id + "_chatlog.pkl"

# save current messages to pkl
with open(message_pickle_location, 'wb') as f:
    pickle.dump(messages, f)


while (isActive and len(messages) <  max_conversation_length):

    # load message history from pkl (function calls update pkl file)
    with open(message_pickle_location, 'rb') as f:
        messages = pickle.load(f)


    # call openAI api
    try:
        chat_response = chat_completion_request(
            messages, tools=tools
        )
    except:
        isActive = False
        isError = True
        print("chat_completion_request error\n")
        continue

    # try to parse the response
    try:
        tool_calls = chat_response.choices[0].message.tool_calls
        messages.append({"role": "assistant", "content": chat_response.choices[0].message.content, "tool_calls": tool_calls})
    except:
        isActive = False
        isError = True
        print("tool_call handling error")
        continue

    # convert messages to pkl file, so it can be fed to tool_call functions:
    with open(message_pickle_location, 'wb') as f:
        pickle.dump(messages, f)


    # early exit if no tool calls are required
    if (tool_calls is None):
        continue
        
    # make tool calls
    for tool_call in tool_calls:
        tool_function_name = tool_call.function.name

        if tool_function_name == "report":
            os.system("python built_in_tools/report.py " + instance_id + " " + tool_call.id)
            isActive = False
            isCallRep = True

        if tool_function_name == "get_current_time":
            os.system("python built_in_tools/get_current_time.py " + instance_id + " " + tool_call.id)
    
    
    while (yetread < len(messages)):
        print(messages[yetread]["role"])
        print(messages[yetread]["content"])
        print("")

        yetread += 1

if (len(messages) ==  max_conversation_length):
    messages.append(
        {
            "role": "system", 
            "content": "Auto-terminated session at " + str(datetime.datetime.now()) + "\nmax_conversation_length exceeded: " + max_conversation_length + "\n"})
    
    with open(message_pickle_location, 'wb') as f:
        pickle.dump(messages, f)
    
