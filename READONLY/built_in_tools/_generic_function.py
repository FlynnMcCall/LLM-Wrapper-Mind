# -- Copy and paste this boilerplate --
# USAGE: (list arguments here)
import sys
import pickle

# returns a pair with the instance_id and tool_call_id
def getCallArgs():
    try:
        instance_id = sys.argv[1]
        tool_call_id = sys.argv[2]
        return [instance_id, tool_call_id]
    except Exception as e:
        print(e)
        print("Error: error accessing sys.argv[1] and sys.argv[2]\n")
        print("Did your call follow 'python  built_in_tools/tool_function_name.py instance_id tool_call_id'?\n")
        exit(1)

# iterates backwards through messages to find last assistant message with a given role
def getLastRoleMessage(messages, role):
    try:
        i = len(messages) - 1
        while(True):
            if (messages[i]["role"] == role):
                return i
            i -= 1
    except Exception as e:
        print("Error. No message found from assistant\n")
        print(e)
        exit(1)

# iterates through a message to find any tool calls matching the give ID. Exits early if not met.
def getToolCallInstance(message, tool_call_id):
    try:
        this_call = None
        tool_calls = message["tool_calls"]
        for tool_call in tool_calls:
            if (tool_call.id == tool_call_id):
                this_call = tool_call
                break
    except Exception as e:
        print(e)
        print("Error, no matching tool_id found in previous message\n")
        print("Could not find tool_id " + tool_call_id + "\n")
        exit(1)
    return this_call





tool_function_name = "FUNCTIONNAME.py"
instance_id, tool_call_id = getCallArgs()

message_pickle_location = "chat_history/" + instance_id + "_chatlog.pkl"
with open(message_pickle_location, 'rb') as f:
    messages = pickle.load(f)

# iterate backwards to find the last message from the assistant
lastRoleMessage = getLastRoleMessage(messages=messages, role="assistant")

# get the instance of this call matching this call id
this_call = getToolCallInstance(message=messages[lastRoleMessage], tool_call_id=tool_call_id)



with open(message_pickle_location, 'wb') as f:
    messages = pickle.dump(messages, f)

