# --Terminates current session. Returns your final message's content to the parent of your current instance.--
# USAGE: python built_in_tools/report.py instance_id tool_call.id
import json
import sys
import datetime
import pickle

message_json_location = "chat_history/" + sys.argv[1] + "_chatlog.json"
message_pickle_location = "chat_history/" + sys.argv[1] + "_chatlog.pkl"
final_report_location = "instance_reports/" + sys.argv[1] + ".report"

"""
with open(message_json_location, 'r') as f:
    messages = json.load(f)
"""

with open(message_pickle_location, 'rb') as f:
    messages = pickle.load(f)

messages.append({
            "role": "tool",
            "tool_call_id": sys.argv[2],
            "content": "Terminated session at " + str(datetime.datetime.now())
            })

# find the final assistant message and copy it to final_report_location
with open(final_report_location, 'w') as f:
    for message in messages[::-1]:
        if (message["role"] == "assistant"):
            content = "No message provided."
            try:
                f.write("ID " + sys.argv[1] + "\nSelf-terminated session at " + str(datetime.datetime.now()) + "\n\n" + message["content"])
            except:
                f.write("ID " + sys.argv[1] + "\nSelf-terminated session at " + str(datetime.datetime.now()) + "\n\n" + "Error, no message provided")
            break

"""
with open(message_json_location, 'w') as f:
    json.dump(messages, f)
"""

with open(message_pickle_location, 'wb') as f:
    messages = pickle.dump(messages, f)
