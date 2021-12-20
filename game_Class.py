from pyautogui import *
import pyautogui, sys
import time
import pandas as pd
import requests
import keyboard
import random
import numpy as np

def functionManaDispo(Turn):
    if int(Turn) == 5:
        return 5.5
    elif int(Turn) == 6:
        return 6
    elif int(Turn) == 7:
        return 6.5
    elif int(Turn) == 8:
        return 7
    elif int(Turn) == 9:
        return 7 + 1 / 3
    elif int(Turn) == 10:
        return 7 + 2 / 3
    elif int(Turn) == 11:
        return 8
    elif int(Turn) == 12:
        return 8 + 1 / 4
    elif int(Turn) == 13:
        return 8 + 2 / 4
    elif int(Turn) == 14:
        return 8 + 3 / 4
    elif int(Turn) == 15:
        return 9
    elif int(Turn) >= 16:
        return 9
    else:
        return int(Turn) + 1

def functionTrickUse(Mana):
    if Mana == 5:
        return 5.5
    elif Mana == 5.5:
        return 6
    elif Mana == 6:
        return 6.5
    elif Mana == 6.5:
        return 7
    elif Mana == 7:
        return 7 + 1 / 3
    elif Mana == 7 + 1 / 3:
        return 7 + 2 / 3
    elif Mana == 7 + 2 / 3:
        return 8
    elif Mana == 8:
        return 8 + 1 / 4
    elif Mana == 8 + 1 / 4:
        return 8 + 2 / 4
    elif Mana == 8 + 2 / 4:
        return 8 + 3 / 4
    elif Mana == 8 + 3 / 4:
        return 9
    elif Mana >= 9:
        return 9
    else:
        return Mana + 1


listTriggers = ["OnDraw", "OnLaying", "OnCharacterAttack", "OnCreatureAttack", "Onkill", "OnUse", "OnDefense", "OnDying", "OnEnemyDamagedBySelf"]
listEvents = ["OnTricksUse", "OnSpellUse", "OnStartTurn", "OnEndTurn", "OnPowerUse", "OnRelicUse", "OnFriendDefense", "OnFriendDamaged", "OnFriendAttack", "OnFriendDies", "OnEnemyDied", "OnEnemyAttack", "OnGodDamaged", "OnGodAttack"]

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
        dicoAlreadyDispatched = {}
        for card, listFunction in self.dicoSubscribers[event].items():
            for function in listFunction:
                
                function(card)  # TODO atention si les fonctions modifie le dico pendant que la boucle for tourne




def Death(player0, player1):
    listDead = []
    for player in [player0, player1]:
        for numCard, card in enumerate(player.Board):
            if card.HealthMax <= card.DamageTaken:
                listDead.append(card)
                if card.Name == "GOD":
                    game.End(1-player.NumPlayer) # TODO régler le pblm de game en argument
                    break
                    break
                print(f'La carte {card.Name} du joueur {player.NumPlayer} est détruite.')
                card.OnBoard = False
                if card.Obliterated:
                    player.Board = [x for x in player.Board if x != card]
                else:
                    card.InVoid = True
                    player.Void.append(player.Board.pop(numCard))
                for event in card.Effects:
                    if event in listEvents: # Les effet peuvent etre des triggers et non des event
                        player.Pub.unregister(event, card)
    # On sépare les boucles for pour activer les afterlife après la destruction des cartes
    for numCard, card in enumerate(listDead):
        if "Afterlife" in card.Property or "Frontline" in card.Property:
            for function in card.Effects["OnDying"]:
                print(f"Apply function of {card.Name}")
                function(card)
        card.Belonging.Pub.dispatch("OnFriendDies")

def GetDamaged(cardDamaged, playerAttacking, Amount):
    if Amount > cardDamaged.Armor:
        cardDamaged.DamageTaken += (Amount - cardDamaged.Armor)
        if "OnDamaged" in cardDamaged.Effects:
            for function in cardDamaged.Effects["OnDamaged"]:
                function(cardDamaged)
        if cardDamaged.Name == "GOD":
            if cardDamaged.Belonging != playerAttacking:
                playerAttacking.Frenzied = True
            cardDamaged.Belonging.Pub.dispatch("OnGodDamaged")
        else:
            cardDamaged.Belonging.Pub.dispatch("OnFriendDamaged")
        print(f'La carte {cardDamaged.Name} subit {Amount - cardDamaged.Armor}, et a mtn {cardDamaged.Health} de vie')
        return True
    else:
        return False

# la fin du tour appelle les carte du board qui on des effets de fin de tour
# use un event pour la fin de tour et utiliser des listener
class Card:
    def __init__(self, possede:int, name:str, mana:int, strength:int, health:int, effects:dict, creature=True, property:list=[], tribu=None, description=""):
        self.Belonging = None
        self.Creature = creature
        self.Name = name
        self.Mana = mana
        self.Strength = strength
        self.HealthMax = health
        self.Tribu = tribu
        self.Description = description
        self.DamageTaken = 0
        self.Effects = effects # on met un dico avec les evenement en clé et la fonction associée
        self.Ready = False # préciser dans les actions possible que le dieu ne peut attaquer
        self.Attackable = False
        self.Property = property
        self.Possede = possede
        self.InDeck = False
        self.InHand = False
        self.OnBoard = False
        self.InVoid = False
        self.Obliterated = False
        self.CanAttackGod = True
        self.Armor = 0 # Ne peut etre negative
        self.Confused = False
        self.Overkill = False
    @property
    def Health(self):
        return self.HealthMax - self.DamageTaken
    def ShowCard(self):
        position = "in Deck"*self.InDeck+"in Hand"*self.InHand+"on Board"*self.OnBoard+"in Void"*self.InVoid+"Obliterated"*self.Obliterated
        print(f'----> Carte {self.Name}, Mana: {self.Mana}, Strength: {self.Strength}, Health: {self.Health}, Property: {self.Property}, Position: {position}'+'\n----> Attackable !'*self.Attackable+'\n----> Ready to play !'*self.Ready)
    def Attack(self, otherPlayer, numCardDefend:int):
        if self.CanAttackGod or numCardDefend!=0:
            if self.Ready and otherPlayer.Board[numCardDefend].Attackable and "Relic" not in self.Property:
                print(f'La carte {self.Name} attaque la carte {otherPlayer.Board[numCardDefend].Name}')
                if GetDamaged(otherPlayer.Board[numCardDefend], self.Belonging, self.Strength):
                    if self.Name == "GOD":
                        self.Belonging.Pub.dispatch("OnGodAttack")
                    if "OnEnemyDamagedBySelf" in self.Effects:
                        for function in self.Effects["OnEnemyDamagedBySelf"]:
                            function(self, otherPlayer.Board[numCardDefend])
                if GetDamaged(self, otherPlayer, otherPlayer.Board[numCardDefend].Strength):
                    if otherPlayer.Board[numCardDefend].Name == "GOD":
                        otherPlayer.Pub.dispatch("OnGodDamaged")
                    if "OnEnemyDamagedBySelf" in otherPlayer.Board[numCardDefend].Effects:
                        for function in otherPlayer.Board[numCardDefend].Effects["OnEnemyDamagedBySelf"]:
                            function(otherPlayer.Board[numCardDefend], self)
                self.Ready = False
                Death(self.Belonging, otherPlayer)
            else:
                print("ERREUR - La carte n'est pas activée ou l'adversaire est inattaquable")
        else:
            print("ERREUR - ne peut pas attaquer le dieu")




class Player:
    def __init__(self, numPlayer:int, begin:bool, deck:list, publisher:Publisher):
        random.shuffle(deck)
        self.NumPlayer = numPlayer
        self.Pub = publisher
        self.Power = 0
        self.ManaDispo = 1
        self.Deck = deck
        self.Void = []
        self.Hand = []
        self.Board = [Card(possede=1, name="GOD", mana=0, strength=0, health=30, effects={}, creature=False)]
        self.Board[0].Belonging = self
        self.Board[0].Attackable = True
        self.Turn = begin
        self.Tricks = begin + 3 * (1 - begin)
        self.TrickUsed = False
        self.Frenzied = False
        self.Relic = None
        print("--------------------------------------------------------------------------------------")
        print(f'Instanciate Player{self.NumPlayer}')
        print("--------------------------------------------------------------------------------------")
    def ShowPlayer(self):
        print(f'----> Player{self.NumPlayer}, Power: {self.Power}, Health: {self.Board[0].Health}, Mana Dispo: {self.ManaDispo}, Hand: {[card.Name for card in self.Hand]}, Board: {[card.Name for i, card in enumerate(self.Board) if i!=0]}, Tricks: {self.Tricks}')
        print(f'-----------------------------------------------------> Mana: {[card.Mana for card in self.Hand]} ----------------------------------- Mana: {[card.Mana for i, card in enumerate(self.Board) if i!=0]}')
        print(f'-------------------------------------------------> Strength: {[card.Strength if "Spell" not in card.Property else "" for card in self.Hand]} ------------------------------- Strength: {[card.Strength if "Spell" not in card.Property else "" for i, card in enumerate(self.Board) if i!=0]}')
        print(f'---------------------------------------------------> Health: {[card.Health if "Spell" not in card.Property else "" for card in self.Hand]} --------------------------------- Health: {[card.Health if "Spell" not in card.Property else "" for i, card in enumerate(self.Board) if i!=0]}')
        print(f'----> His Turn to play !'*self.Turn)
    def EndTurn(self, otherPlayer, game):
        game.EndTurn(playerEnding = self, playerStarting = otherPlayer)
    def Draw(self, nbrCards):
        nbrCardsDraw = 0
        for i in range(nbrCards):
            if len(self.Deck) != 0:
                self.Hand.append(self.Deck.pop(0))
                self.Hand[-1].InHand = True
                self.Hand[-1].InDeck = False
                self.Hand[-1].Belonging = self
                nbrCardsDraw += 1
            else:
                print("Plus de cartes a tirer")
        print(f'Player{self.NumPlayer} drew {nbrCardsDraw} Cards, named: {[card.Name for card in self.Hand[-nbrCardsDraw:]]}')
    def UseAbility(self, numCardOnBoard:int=None, relic=False):
        if relic and self.Relic!=None:
            if "OnUse" in self.Relic.Effects and self.Relic.Ready:
                for function in self.Relic.Effects["OnUse"]:
                    function(self.Relic)
                if self.Relic != None:
                    self.Relic.Ready = False
            else:
                print("ERREUR - Impossible d'utiliser la relic")
        elif numCardOnBoard>=0 and numCardOnBoard<len(self.Board):
                if "OnUse" in self.Board[numCardOnBoard].Effects and "Ability" in self.Board[numCardOnBoard].Property and self.Board[numCardOnBoard].Ready:
                    for function in self.Board[numCardOnBoard].Effects["OnUse"]:
                        function(self.Board[numCardOnBoard])
                    self.Board[numCardOnBoard].Ready = False # TODO ajuster le cas où l'ability autodétruit la carte , elle ne peut plus etre mis a ready false
                else:
                    print("ERREUR - Aucune Ability")
        else:
            print("ERREUR - Aucune carte")
    def LayCard(self, numCardInHand:int):
        if numCardInHand >= 0 and numCardInHand < len(self.Hand):
            if self.Hand[numCardInHand].Mana <= self.ManaDispo:
                if "Relic" in self.Hand[numCardInHand].Property:
                    if self.Relic != None:
                        self.Void.append(self.Relic)
                        print(f"La relic {self.Relic.Name} est détruite")
                    self.Hand[numCardInHand].InHand = False
                    self.Hand[numCardInHand].Belonging = self
                    self.ManaDispo -= self.Hand[numCardInHand].Mana
                    self.Relic = self.Hand[numCardInHand]
                    print(f'Player{self.NumPlayer} play a Relic, named: {self.Hand[numCardInHand].Name}, with {self.Hand[numCardInHand].Mana} Mana')
                    if "OnLaying" in self.Relic.Effects:
                        for function in self.Relic.Effects["OnLaying"]:
                            function(self.Relic)
                    self.Hand.pop(numCardInHand)
                elif "Spell" in self.Hand[numCardInHand].Property:
                    self.Void.append(self.Hand.pop(numCardInHand))
                    self.Void[-1].InHand = False
                    self.Void[-1].InVoid = True
                    self.Void[-1].Belonging = self
                    self.ManaDispo -= self.Void[-1].Mana
                    if "OnLaying" in self.Void[-1].Effects:
                        for function in self.Void[-1].Effects["OnLaying"]:
                            function(self.Void[-1])
                    print(f'Player{self.NumPlayer} play a Spell, named: {self.Void[-1].Name}, with {self.Void[-1].Mana} Mana')
                elif len(self.Board) <= 6:
                    self.Board.append(self.Hand.pop(numCardInHand))
                    self.Board[-1].InHand = False
                    self.Board[-1].OnBoard = True
                    self.Board[-1].Belonging = self
                    self.ManaDispo -= self.Board[-1].Mana
                    # On register les effect de la carte aux events quand on la pose
                    if "OnLaying" in self.Board[-1].Effects:
                        for function in self.Board[-1].Effects["OnLaying"]:
                            function(self.Board[-1])
                    for event in listEvents: # TODO des effets s'active dans ta mains, ajouter leur activation au tirage
                        if event in self.Board[-1].Effects:
                            self.Pub.register(event, self.Board[-1])
                    print(f'Player{self.NumPlayer} lay a Card, named: {self.Board[-1].Name}, with {self.Board[-1].Mana} Mana')
                else:
                    print("ERREUR - Le board est plein !")
            else:
                print(f"ERREUR - Vous n'avez que {self.ManaDispo} de Mana dispo, vous ne pouvez une carte de {self.Hand[numCardInHand].Mana} Mana")
        else:
            print("ERREUR - Aucune carte a cette position")
    def UseTricks(self):
        if self.Tricks > 0 and self.TrickUsed == False:
            self.Tricks -= 1
            self.ManaDispo = functionTrickUse(self.ManaDispo)
            self.TrickUsed = True
            print(f'Player{self.NumPlayer} used a trick, he has now {self.ManaDispo} Mana')
        else:
            print('ERREUR - Plus de tricks, ou déjà utilisé')
    def AttackWithCard(self, otherPlayer, numCardAttack:int, numCardDefend:int):
        if numCardAttack >=0 and numCardAttack < len(self.Board):
            if "Ability" not in self.Board[numCardAttack].Property:
                # Confused
                if self.Board[numCardAttack].Confused:
                    if len([numCard for numCard in range(len(otherPlayer.Board)) if numCardDefend != numCard and otherPlayer.Board[numCard].Attackable]) != 0:
                        numCardDefend = random.choice([numCardDefend, random.choice([numCard for numCard in range(len(otherPlayer.Board)) if numCardDefend != numCard and otherPlayer.Board[numCard].Attackable])])

                self.Board[numCardAttack].Attack(otherPlayer, numCardDefend)
                Death(self, otherPlayer)
            else:
                print("ERREUR - Les cartes avec Ability ne peuvent attaquer")
        else:
            print(f'ERREUR - Ancune carte pour attaquer')


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
        playerStarting.TrickUsed = False
        self.Turn += 0.5
        playerStarting.ManaDispo = functionManaDispo(self.Turn)
        for card in playerEnding.Board:
            card.Attackable = True
        for card in playerStarting.Board[1:]:
            card.Ready = True
            card.CanAttackGod = True
        if playerStarting.Relic != None:
            playerStarting.Relic.Ready = True
        playerStarting.Frenzied = False
        playerEnding.Pub.dispatch("OnEndTurn")
        playerStarting.Pub.dispatch("OnStartTurn")
        print(f'Player{playerEnding.NumPlayer} ended turn, GameTurn: {self.Turn}')
        playerStarting.Draw(nbrCards=1)
        playerStarting.ShowPlayer()
    def End(self, winner:int):
        self.NumGame += 1
        self.Victories[winner] += 1
        self.Times.append(time.time() - self.StartTime)
        self.Turns.append(self.Turn)
        self.Running = False
        self.StartTime = None
        self.Turn = 0
        print(f"Le joueur {winner} gagne !!")
        # TODO réinitialiser le jeux

class Strategy:
    def __init__(self):
        pass













# TODO est ce que quand on remplace une relic ses effets (afterlife) s'appliquent ??










