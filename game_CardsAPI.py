from pyautogui import *
import pyautogui, sys
import time
import pandas as pd
import requests
import keyboard
import random
import numpy as np

listTypeEffect = ["Ability", "Afterlife", "Backline", "Blessed", "Blitz", "Burn", "Confused", "Deadly", "Flank",
                  "Frontline", "Godblitz", "Hidden", "Leech", "Overkill", "Obliterate", "Protected", "Regen",
                  "Roar", "Sleep", "Souless", "Summon", "Twin strike", "Ward"]

# API pour récup les 1200 cartes
response = requests.get('https://api.godsunchained.com/v0/proto?page=1&perPage=3000')
Existingcards = pd.DataFrame(response.json()['records']).sort_values(by="name", ignore_index=True)
for index in Existingcards.index:
    Existingcards.loc[index, "tribe"] = dict(Existingcards.loc[index, "tribe"])['String']
    Existingcards.loc[index, "attack"] = dict(Existingcards.loc[index, "attack"])['Int64']
    Existingcards.loc[index, "health"] = dict(Existingcards.loc[index, "health"])['Int64']

Existingcards = Existingcards.sort_values(by="effect", ignore_index=True)
baseTypeEffects = pd.DataFrame()
baseTriggerEffects = pd.DataFrame()
Existingcards["typeEffect"] = ""
Existingcards["TriggerEffect"] = ""
for index in Existingcards.index:
    baseTypeEffects.loc[index, "effect"] = Existingcards.loc[index, "effect"]
    for effect in listTypeEffect:
        if effect in Existingcards.loc[index, "effect"]:
            baseTypeEffects.loc[index, effect] = 1
            Existingcards.loc[index, "typeEffect"] = Existingcards.loc[index, "typeEffect"] + effect + " / "
            if effect in ["Burn", "Deadly", "Flank", "Leech", "Overkill"]:
                baseTriggerEffects.loc[index, "OnCaracterAttack"] = 1
                Existingcards.loc[index, "TriggerEffect"] + "OnCaracterAttack" + " / "
        else:
            baseTypeEffects.loc[index, effect] = 0

# Existingcards.to_csv("C:/Users/C00000404/PycharmProjects/BotGU/csv/Existingcards.csv")












