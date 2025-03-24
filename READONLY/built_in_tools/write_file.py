# -- Copy and paste this boilerplate --
# USAGE: (list arguments here)
import json
import sys
import datetime
import pickle

message_pickle_location = "chat_history/" + sys.argv[1] + "_chatlog.pkl"

with open(message_pickle_location, 'rb') as f:
    messages = pickle.load(f)

messages[:-1]


with open(message_pickle_location, 'wb') as f:
    messages = pickle.dump(messages, f)

