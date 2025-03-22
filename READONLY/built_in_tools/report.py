# --Terminates current session. Returns your final message's content to the parent of your current instance.--
# USAGE: python built_in_tools/report.py instance_id tool_call.id
import json
import sys
import datetime

message_json_location = "chat_history/" + sys.argv[1] + "_chatlog.json"
final_report_location = "instance_reports/" + sys.argv[1] + ".report"

with open(message_json_location, 'r') as f:
    messages = json.load(f)

messages.append({
            "role": "tool",
            "tool_call_id": sys.argv[2],
            "content": "Terminated session at " + str(datetime.datetime.now())
            })

# find the final assistant message and copy it to final_report_location
with open(final_report_location, 'r') as f:
    for message in messages[::-1]:
        if (message["role"] == "assistant"):
            content = "No message provided."
            try:
                f.write(message["content"] + "\n\nSelf-terminated session at " + str(datetime.datetime.now()))
            except:
                f.write("Error, no final message provided." + "\n\nTerminated session at " + str(datetime.datetime.now()))
            break


with open(message_json_location, 'w') as f:
    json.dump(messages, f)

