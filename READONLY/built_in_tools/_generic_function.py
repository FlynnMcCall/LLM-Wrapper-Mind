# -- Copy and paste this boilerplate --
# USAGE: (list arguments here)
import json
import sys
import datetime
import pickle

message_pickle_location = "chat_history/" + sys.argv[1] + "_chatlog.pkl"

with open(message_pickle_location, 'rb') as f:
    messages = pickle.load(f)

args = json.loads(messages[-1].function.arguments)


with open(message_pickle_location, 'wb') as f:
    messages = pickle.dump(messages, f)

