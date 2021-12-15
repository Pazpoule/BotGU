from pyautogui import *
import pyautogui, sys
import time
import pandas as pd
import requests
import keyboard
import random
import numpy as np
from game_Class import *


listTriggers = ["OnDraw", "OnLaying", "OnCharacterAttack", "OnGodAttack", "OnCreatureAttack", "Onkill", "OnUse",
                "OnDefense", "OnDying", "OnEnemyDamagedBySelf"]
listEvents = ["OnTricksUse", "OnSpellUse", "OnStartTurn", "OnEndTurn", "OnPowerUse", "OnRelicUse", "OnFriendDefense", "OnFriendDamaged"
              "OnFriendAttack", "OnFriendDies", "OnEnemyDied", "OnEnemyAttack"]

listTypeEffect = ["Ability", "Afterlife", "Backline", "Blessed", "Blitz", "Burn", "Confused", "Deadly", "Flank",
                  "Frontline", "Godblitz", "Hidden", "Leech", "Overkill", "Obliterate", "Protected", "Regen",
                  "Roar", "Sleep", "Souless", "Summon", "Twin strike", "Ward"]


def sortPlayers(player0, player1):
    if player0.Turn:
        return [player0, player1]
    else:
        return [player1, player0]

def Frontline(card):
    player = card.Belonging
    if [1 for card in player.Board if "Frontline" in card.Property]:
        for card in player.Board:
            if "Frontline" not in card.Property:
                card.Attackable = False
                print(f"La carte {card.Name} est non attackable")
        player.Attackable = False
        print("y a Frontline")
    else:
        for card in player.Board:
            if "Hidden" not in card.Property and "Backline" not in card.Property or (
                    "Backline" in card.Property and not [1 for card in player.Board if
                                                         "Backline" not in card.Property]):
                card.Attackable = True
        player.Attackable = True
        print("y a plus Frontline")

def Backline(card):
    player = card.Belonging
    if [1 for card in player.Board if "Backline" not in card.Property]:
        for card in player.Board:
            if "Backline" in card.Property:
                card.Attackable = False
                print(f"La carte {card.Name} est non attackable")
    else:
        for card in player.Board:
            card.Attackable = True
            print(f"La carte {card.Name} est non attackable")

def Summon(card, creatureSummoned, opponent=False):
    player = card.Belonging
    if opponent:
        player = player0 if player == player1 else player1
    if len(player.Board) < 6:
        player.Board.append(creatureSummoned)
        player.Board[-1].OnBoard = True
        print(f"Le board du joueur {player.NumPlayer} gagne la carte {creatureSummoned.Name}")
    else:
        print("Summon impossible, le board est plein")

def AddInDeck(card, cardAdded, opponent=False, position=None):
    player = card.Belonging
    if opponent:
        player = player0 if player == player1 else player1
    if position==None:
        position = random.randrange(0, len(player.Deck))
    player.Deck.insert(position, cardAdded)
    print(f"La carte {cardAdded.Name} a été ajouté au deck du joueur {player.NumPlayer}")

def ModifyStats(card, strength, healthMax, damageTaken=0, opponent=False, specifyCard=None):
    player = card.Belonging
    if opponent:
        player = player0 if player == player1 else player1
    if specifyCard == None:
        print("Entrer le numero de la carte")
        numCard = int(input())
        try:
            modifiedCard = player.Board[numCard]
        except:
            print("Carte non trouvée")
    else:
        modifiedCard = specifyCard
    try:
        modifiedCard.Strength += strength
        modifiedCard.HealthMax += healthMax
        modifiedCard.DamageTaken *= damageTaken
        print(f"La carte {modifiedCard.Name} est modifiée de {strength}/{healthMax-damageTaken} et a maintenant des stats de {modifiedCard.Strength}/{modifiedCard.Health}")
        Death(player0, player1)
    except:
        print("ERREUR -- ModifyStats")

def Blitz(card):
    player = card.Belonging
    player.Board[-1].Ready = True
    print(f"La carte {player.Board[-1].Name} a Blitz et peut attaquer")

def GetConfused(card, toSelf=True, opponent=False, specifyCard=None):
    if toSelf:
        card.Confused = True
        print(f"La carte {card.Name} devient confused")
    else:
        player = card.Belonging
        if opponent:
            player = player0 if player == player1 else player1
        if specifyCard == None:
            print("Entrer le numero de la carte")
            numCard = int(input())
            player.Board[numCard].Confused = True
            print(f"La carte {player.Board[numCard].Name} devient confused")
        else:
            specifyCard.Confused = True
            print(f"La carte {specifyCard.Name} devient confused")

def Overkill(card):
    pass

 # TODO ne pas modif la vie mais mettre un attribu dommage subis

if __name__ == '__main__':


    ToAddInDeck = Card(1, "ToAddInDeck", 0, 1, 1, {})
    Impling = Card(1, "Impling", 0, 1, 1, {})
    carte1 = Card(1, "1", 1, 2, 2, {"OnEndTurn": lambda self: Frontline(self), "OnDying": lambda self: Frontline(self)}, property=["Frontline"])
    carte2 = Card(1, "2", 1, 1, 3, {"OnLaying": lambda self: ModifyStats(self, 0, -1, opponent=True)})
    carte3 = Card(1, "3", 1, 3, 3, {"OnEndTurn": lambda self: Frontline(self), "OnDying": lambda self: Frontline(self)}, property=["Frontline"]) # verif le OnDying de la frontline
    carte4 = Card(1, "4", 1, 2, 4, {"OnEndTurn": lambda self: Backline(self), "OnFriendDies": lambda self: Backline(self)}, property=["Backline"])
    carte5 = Card(1, "5", 1, 3, 1, {"OnDying": lambda self: Summon(self, Impling)}, property=["Afterlife"]) # TODO pblm si l'ennemie detruit la carte, summon regarde en fonction de turn qui est a faux
    carte6 = Card(1, "6", 1, 3, 4, {"OnLaying": lambda self: ModifyStats(self, 1, 1)})
    carte7 = Card(1, "7", 1, 4, 4, {"OnLaying": lambda self: Blitz(self)}, property=["Blitz"])
    carte8 = Card(1, "8", 1, 4, 5, {"OnLaying": lambda self: AddInDeck(self, ToAddInDeck)}, property=["Roar"])
    carte9 = Card(1, "9", 1, 1, 4, {"OnEnemyDamagedBySelf": lambda self, opponentCard: ModifyStats(self, -1, 0, opponent=True, specifyCard=opponentCard)})
    carte10 = Card(1, "10", 1, 6, 6, {"OnLaying": lambda self: GetConfused(self)}, property=["Confused"])
    pub0 = Publisher(listEvents)
    pub1 = Publisher(listEvents)
    global player0, player1
    player0 = Player(0, True, deck = [carte1, carte3, carte5, carte7, carte9], publisher=pub0)
    player1 = Player(1, False, deck = [carte2, carte4, carte6, carte8, carte10], publisher=pub1)

    game = Game()
    game.Start(player0, player1)


    # player0.LayCard(1)
    # player1.LayCard(0) # TODO demander les numplayer et num card en unput dans les fonction !!!!!!!!!!!!!!!!!!!!!
    # player1.LayCard(3, player0, 0)
    #
    # player0.EndTurn(player1, game)
    # player1.EndTurn(player0, game)
    #
    # player0.AttackCard(player1, 0, 0)
    # player1.AttackCard(player0, 0, 0)
    #
    # player0.ShowPlayer()
    # player1.ShowPlayer()
    #
    # player0.UseTricks()
    # player1.UseTricks()




    # TODO gérer les pop on end list








    # TODO rechercher combien d'exemplaire d'une carte on peut mettre par Deck en ft de la rareté

    # TODO favors

    # TODO gerer l'arrvée en fin de list ie fin de deck


    # strategy = Strategy()
    # player0 = Player()
    # player1 = Player()
    # game = Game(player0, player1)
    # game.Start()
    # while game.Running:
    #     if listPayer[0].Turn:
    #         strategy(0)
    #     else:
    #         strategy(1)
    #     if listPayer[0].Dead:
    #         game.End(winner=1)
    #     elif listPayer[1].Dead:
    #         game.End(winner=0)























