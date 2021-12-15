from pyautogui import *
import pyautogui, sys
import time
import pandas as pd
import requests
import keyboard
import random
import numpy as np


listTriggers = ["OnDraw", "OnLaying", "OnCharacterAttack", "OnGodAttack", "OnCreatureAttack", "Onkill", "OnUse",
                "OnDefense", "OnDying", "OnEnemyDamagedBySelf"]
listEvents = ["OnTricksUse", "OnSpellUse", "OnStartTurn", "OnEndTurn", "OnPowerUse", "OnRelicUse", "OnFriendDefense", "OnFriendDamaged"
              "OnFriendAttack", "OnFriendDies", "OnEnemyDied", "OnEnemyAttack"]

class Publisher: # on créer un publisher par player
    def __init__(self, listEvents):
        self.dicoSubscribers = {event:dict() for event in listEvents}
    def register(self, event, card):
        self.dicoSubscribers[event][card] = card.Effects[event]
        print(f"Registered card {card.Name} for the event {event}")
    def unregister(self, event, card):
        del self.dicoSubscribers[event][card]
        print(f"Unregistered card {card.Name} for the event {event}")
    def dispatch(self, event):
        for card, function in self.dicoSubscribers[event].items():
            function(card)

def Death(player0, player1):
    for player in [player0, player1]:
        for numCard, card in enumerate(player.Board):
            if card.HealthMax <= card.DammageTaken:
                print(f'La carte {card.Name} du joueur {player.NumPlayer} est détruite.')
                card.OnBoard = False
                card.InVoid = True  # TODO if obliterated
                player.Void.append(player.Board.pop(numCard))
                for event in card.Effects:
                    if event in listEvents: # Les effet peuvent etre des triggers et non des event
                        player.Pub.unregister(event, card)
                player.Pub.dispatch("OnFriendDies")
                if "Afterlife" in card.Property or "Frontline" in card.Property:
                    card.Effects["OnDying"](card)

def GetDamaged(cardDamaged, Amount):
    if Amount > cardDamaged.Armor:
        cardDamaged.DamageTaken += (Amount - cardDamaged.Armor)
        if "OnDamaged" in cardDamaged.Effects:
            cardDamaged.Effects["OnDamaged"](cardDamaged)
        cardDamaged.Belonging.Pub.dispatch("OnFriendDamaged")
        return True
    else:
        return False

# TODO la class cards doit avoir une methode par pouvoir et une methode attack, la class player appelle la class cards pour attacker
# la fin du tour appelle les carte du board qui on des effets de fin de tour
# use un event pour la fin de tour et utiliser des listener
class Card:
    def __init__(self, possede:int, name:str, mana:int, strength:int, health:int, effects:dict, property:list=[]):
        self.Name = name
        self.Mana = mana
        self.Strength = strength
        self.HealthMax = health
        self.DamageTaken = 0
        self.Triggers = None # TOdo
        self.Effects = effects # on met un dico avec les evenement en clé et la fonction associée
        self.Ready = False
        self.Attackable = False
        self.Property = property
        self.Possede = possede
        self.InDeck = False
        self.InHand = False
        self.OnBoard = False
        self.InVoid = False
        self.Obliterated = False
        self.Belonging = None
        self.Armor = 0 # Ne peut etre negative
        self.Confused = False
        self.Overkill = False
        print("--------------------------------------------------------------------------------------")
        print(f'Instanciate Card, name: {self.Name}, Mana: {self.Mana}, Strength: {self.Strength}, Health: {self.HealthMax}')
        print("--------------------------------------------------------------------------------------")
    @property
    def Health(self):
        return self.HealthMax - self.DamageTaken
    def ShowCard(self):
        position = "in Deck"*self.InDeck+"in Hand"*self.InHand+"on Board"*self.OnBoard+"in Void"*self.InVoid+"Obliterated"*self.Obliterated
        print(f'----> Carte {self.Name}, Mana: {self.Mana}, Strength: {self.Strength}, Health: {self.Health}, Property: {self.Property}, Position: {position}'+'\n----> Attackable !'*self.Attackable+'\n----> Ready to play !'*self.Ready)
    def AttackCard(self, otherPlayer, numCardDefend:int):
        if self.Ready:
            print(f'La carte {self.Name} attaque la carte {otherPlayer.Board[numCardDefend].Name}')
            if GetDamaged(otherPlayer.Board[numCardDefend], self.Strength):
                if "OnEnemyDamagedBySelf" in self.Effects:
                    self.Effects["OnEnemyDamagedBySelf"](self, otherPlayer.Board[numCardDefend])
            if GetDamaged(self, otherPlayer.Board[numCardDefend].Strength):
                if "OnEnemyDamagedBySelf" in otherPlayer.Board[numCardDefend].Effects:
                    otherPlayer.Board[numCardDefend].Effects["OnEnemyDamagedBySelf"](otherPlayer.Board[numCardDefend], self)
            self.Ready = False
        else:
            print("ERREUR - La carte n'est pas activée, attaque impossible")



class Player:
    def __init__(self, numPlayer:int, begin:bool, deck:list, publisher:Publisher):
        random.shuffle(deck)
        self.NumPlayer = numPlayer
        self.Pub = publisher
        self.Power = 0
        self.Health = 30
        self.ManaDispo = 1
        self.Deck = deck
        self.Void = []
        self.Hand = []
        self.Board = []
        self.Turn = begin
        self.Tricks = begin + 3 * (1 - begin)
        self.Attackable = False
        print("--------------------------------------------------------------------------------------")
        print(f'Instanciate Player{self.NumPlayer}, Health: {self.Health}, his Turn to play: {self.Turn}')
        print("--------------------------------------------------------------------------------------")
    def ShowPlayer(self):
        print(f'----> Player{self.NumPlayer}, Power: {self.Power}, Health: {self.Health}, Mana Dispo: {self.ManaDispo}, Hand: {[card.Name for card in self.Hand]}, Board: {[card.Name for card in self.Board]}, Tricks: {self.Tricks}')
        print(f'-----------------------------------------------------> Mana: {[card.Mana for card in self.Hand]} ----------------------------------- Mana: {[card.Mana for card in self.Board]}')
        print(f'-------------------------------------------------> Strength: {[card.Strength for card in self.Hand]} ------------------------------- Strength: {[card.Strength for card in self.Board]}')
        print(f'---------------------------------------------------> Health: {[card.Health for card in self.Hand]} --------------------------------- Health: {[card.Health for card in self.Board]}')
        print(f'----> His Turn to play !'*self.Turn)
    def EndTurn(self, otherPlayer, game):
        game.EndTurn(playerEnding = self, playerStarting = otherPlayer)
    def Draw(self, nbrCards):
        for i in range(nbrCards):
            self.Hand.append(self.Deck.pop(0))
            self.Hand[-1].InHand = True
            self.Hand[-1].InDeck = False
            self.Hand[-1].Belonging = self
        print(f'Player{self.NumPlayer} drew {nbrCards} Cards, named: {[card.Name for card in self.Hand[-nbrCards:]]}')
    def LayCard(self, numCardInHand:int):
        if self.Hand[numCardInHand].Mana <= self.ManaDispo: # TODO si le board est plein
            self.Board.append(self.Hand.pop(numCardInHand))
            self.Board[-1].InHand = False
            self.Board[-1].OnBoard = True
            self.Board[-1].Belonging = self
            self.ManaDispo -= self.Board[-1].Mana
            # On register les effect de la carte aux events quand on la pose
            for event in listEvents:
                if event in self.Board[-1].Effects:
                    self.Pub.register(event, self.Board[-1])
            if "OnLaying" in self.Board[-1].Effects:
                self.Board[-1].Effects["OnLaying"](self.Board[-1])
            print(f'Player{self.NumPlayer} lay a Card, named: {self.Board[-1].Name}, with {self.Board[-1].Mana} Mana')
        else:
            print(f"ERREUR - Vous n'avez que {self.ManaDispo} de Mana dispo, vous ne pouvez une carte de {self.Hand[numCardInHand].Mana} Mana")
    def UseTricks(self):
        if self.Tricks > 0:
            self.Tricks -= 1
            self.ManaDispo += 1
            print(f'Player{self.NumPlayer} used a trick, he has now {self.ManaDispo} Mana')
        else:
            print('ERREUR - Plus de tricks')
    def AttackCard(self, otherPlayer, numCardAttack:int, numCardDefend:int): # TODO gerer l'attack god dans confused et overkill
        if self.Board[numCardAttack].Confused:
            if len([numCard for numCard in range(len(otherPlayer.Board)) if (numCard != numCardDefend and otherPlayer.Board[numCard].Attackable)]) != 0:
                numCardDefend = random.choice([numCardDefend, random.choice([numCard for numCard in range(len(otherPlayer.Board)) if (numCard != numCardDefend and otherPlayer.Board[numCard].Attackable)])])
        if self.Board[numCardAttack].Overkill:
            surplus = self.Board[numCardAttack].Strengh - (otherPlayer.Board[numCardDefend].Health + otherPlayer.Board[numCardDefend].Armor)
            if surplus > 0:
                for damage in range(surplus):
                    pass
        if otherPlayer.Board[numCardDefend].Attackable:
            self.Board[numCardAttack].AttackCard(otherPlayer, numCardDefend)
        else:
            print("ERREUR - La carte de l'adversaire est non attackable")
        Death(self, otherPlayer)
    def AttackGod(self, otherPlayer, numCardAttack:int): # TODO gerer l'attack d'un god ---------------
        otherPlayer.Health -= self.Board[numCardAttack].Strength
        self.Board[numCardAttack].Ready = False
        print(f'La carte {self.Board[numCardAttack].Name} attaque le dieu du joueur {1 - self.NumPlayer}')

class Game:
    def __init__(self):
        self.NumGame = 0
        self.Victories = [0, 0]
        self.Times = []
        self.Turns = []
        self.Running = False
        self.StartTime = None
        self.Turn = 0
        print("--------------------------------------------------------------------------------------")
        print(f'Instanciate Game numero {self.NumGame}, Victoires: {self.Victories}, Temps: {self.Times}, Turns: {self.Turns}'+f'\nRUNNING !'*self.Running)
        print("--------------------------------------------------------------------------------------")
    def ShowGame(self):
        print(f'----> Game numero {self.NumGame}, Victoires: {self.Victories}, Temps: {self.Times}, Turns: {self.Turns}'+f'\nRUNNING !'*self.Running)
    def Start(self, player0, player1):
        self.Running = True
        self.StartTime = time.time()
        player0.Draw(nbrCards=4*player0.Turn + 3*(1-player0.Turn))
        player1.Draw(nbrCards=4*player1.Turn + 3*(1-player1.Turn))
        player0.ManaDispo = 1
        player1.ManaDispo = 1
        print(f'Game Running !')
        if player0.Turn:
            player0.ShowPlayer()
        else:
            player1.ShowPlayer()
    def EndTurn(self, playerEnding, playerStarting):
        playerEnding.Turn = False
        playerStarting.Turn = True
        self.Turn += 0.5
        playerStarting.ManaDispo = int(self.Turn) + 1
        for card in playerEnding.Board:
            card.Attackable = True
        for card in playerStarting.Board:
            card.Ready = True
        playerEnding.Pub.dispatch("OnEndTurn")
        playerStarting.Pub.dispatch("OnStartTurn")
        print(f'Player{playerEnding.NumPlayer} ended turn, GameTurn: {self.Turn}')
        playerStarting.Draw(nbrCards=1)
        # TODO régler l'augmentation progressive de la mana apres le tour 5 et impact sur tricks
        playerStarting.ShowPlayer()
    def End(self, winner:int):
        self.NumGame += 1
        self.Victories[winner] += 1
        self.Times.append(time.time() - self.StartTime)
        self.Turns.append(self.Turn)
        self.Running = False
        self.StartTime = None
        self.Turn = 0

class Strategy:
    def __init__(self):
        pass

























