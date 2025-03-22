# --Returns the current time in Y-m-d H:M:S format--
# USAGE: python built_in_tools/get_current_time.py instance_id tool_call.id
import json
import sys
import datetime

message_json_location = "chat_history/" + sys.argv[1] + "_chatlog.json"

with open(message_json_location, 'r') as f:
    messages = json.load(f)

messages.append({
            "role": "tool",
            "tool_call_id": sys.argv[2],
            "content": str(datetime.datetime.now())
            })

with open(message_json_location, 'w') as f:
    json.dump(messages, f)

