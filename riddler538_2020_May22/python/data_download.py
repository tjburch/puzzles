#!/usr/bin/python
from urllib.request import urlopen
import pickle
import os

SAVEDIR = os.getcwd().split("python")[0]+"/data/" if "python" in os.getcwd() else os.getcwd()+"/data/"
print(f"Saving in {SAVEDIR}")
#opening a file like object using urllib
webpage= urlopen("https://norvig.com/ngrams/word.list")

wordlist = []

for line in webpage.readlines():
    wordlist.append(line.rstrip())

print(wordlist[0:30])
#creating our output file

with open(SAVEDIR+"/word-list.pkl", "wb") as f:
    pickle.dump(wordlist, f)


## States
states = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming"
]

with open(SAVEDIR+"/state-list.pkl", "wb") as f:
    pickle.dump(states, f)
