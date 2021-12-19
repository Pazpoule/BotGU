from pyautogui import *
import pyautogui, sys
import time
import pandas as pd
import requests
import keyboard
import random
import numpy as np
from game_Class import *

listTypeEffect = ["Ability", "Afterlife", "Backline", "Blessed", "Blitz", "Burn", "Confused", "Deadly", "Flank", "Frontline", "Godblitz", "Hidden", "Leech", "Overkill", "Obliterate", "Protected", "Regen", "Roar", "Sleep", "Souless", "Summon", "Twin strike", "Ward"]


def OpposingPlayer(player):
    for joueur in [player0, player1]:
        if joueur != player:
            return joueur

def Frontline(card):
    player = card.Belonging
    if [1 for card in player.Board if "Frontline" in card.Property]:
        for card in player.Board:
            if "Frontline" not in card.Property:
                card.Attackable = False
                print(f"La carte {card.Name} est non attackable")
        print("y a Frontline")
    else:
        for card in player.Board:
            if "Hidden" not in card.Property and "Backline" not in card.Property or ("Backline" in card.Property and not [1 for card in player.Board if "Backline" not in card.Property]):
                card.Attackable = True
        print("y a plus Frontline")

def Backline(card):
    player = card.Belonging
    if [1 for i, card in enumerate(player.Board) if i!=0 and "Backline" not in card.Property]:
        for card in player.Board:
            if "Backline" in card.Property:
                card.Attackable = False
                print(f"La carte {card.Name} est non attackable")
    else:
        for card in player.Board: # TODO gérer les hidden etc
            card.Attackable = True
            print(f"La carte {card.Name} est attackable")

def Summon(card, creatureSummoned, opponent=False):
    player = card.Belonging
    if opponent:
        player = player0 if player == player1 else player1
    if len(player.Board) <= 6:
        player.Board.append(creatureSummoned)
        player.Board[-1].Belonging = player
        player.Board[-1].OnBoard = True
        print(f"Le board du joueur {player.NumPlayer} gagne la carte {creatureSummoned.Name}")
    else:
        print("Summon impossible, le board est plein")

def AddInDeck(card, cardAdded, opponent=False, position=None):
    player = card.Belonging
    if opponent:
        player = player0 if player == player1 else player1
    if position==None:
        if len(player.Deck)==0:
            position = 0
        else:
            position = random.randrange(0, len(player.Deck))
    player.Deck.insert(position, cardAdded)
    print(f"La carte {cardAdded.Name} a été ajouté au deck du joueur {player.NumPlayer}")

def ModifyStats(card, strength, healthMax, damageTaken=0, opponent=False, specifyCard=None, selfApplicable=False, toCreature=True):
    player = card.Belonging
    if opponent:
        player = player0 if player == player1 else player1
    if (toCreature and len(player.Board) > 1+(1-selfApplicable)-opponent) or not toCreature:
        if specifyCard == None:
            numCard = -1
            while True:
                while (numCard < 0 or numCard >= len(player.Board)) or (toCreature and numCard==0):
                    print("Entrer le numero de la carte")
                    numCard = int(input())
                if selfApplicable or player.Board[numCard] != card:
                    break
                else:
                    print("La carte n'est pas applicable a elle même")
                    numCard = -1
            modifiedCard = player.Board[numCard]
        else:
            modifiedCard = specifyCard
        modifiedCard.Strength += strength
        if modifiedCard.Strength < 0:
            modifiedCard.Strength = 0
        modifiedCard.HealthMax += healthMax
        if damageTaken >0:
            GetDamaged(modifiedCard, card.Belonging, damageTaken)
        print(f"La carte {modifiedCard.Name} est modifiée de {strength}/{healthMax-damageTaken} et a maintenant des stats de {modifiedCard.Strength}/{modifiedCard.Health}")
        Death(player0, player1)
    else:
        print("Aucune carte a modifier")


def Blitz(card):
    player = card.Belonging
    player.Board[-1].Ready = True
    player.Board[-1].CanAttackGod = False
    print(f"La carte {player.Board[-1].Name} a Blitz et peut attaquer")

def GetConfused(card, toSelf=True, opponent=False, specifyCard=None):
    if toSelf:
        specifyCard = card
    else:
        player = card.Belonging
        if opponent:
            player = player0 if player == player1 else player1
        if specifyCard == None:
            numCard = -1
            while numCard < 1 or numCard >= len(player.Board):
                print("Entrer le numero de la carte")
                numCard = int(input())
            specifyCard = player.Board[numCard]
    specifyCard.Confused = True
    print(f"La carte {specifyCard.Name} devient confused")

def Overkill(card):
    pass

def ModifyDurability(card, Amount, opponent=True): # Amount >0 remove durability
    player = card.Belonging
    if opponent:
        player = player0 if player == player1 else player1
    relicCard = player.Relic
    relicCard.DamageTaken += Amount
    if "OnLooseDurability" in relicCard.Effects and Amount > 0:
        for function in relicCard.Effects["OnLooseDurability"]:
            function(relicCard)
    if relicCard.Health <= 0:
        player.Void.append(relicCard)
        player.Relic = None
        print(f"Relic {relicCard.Name} removed")
        if "Afterlife" in relicCard.Property:
            for function in relicCard.Effects["OnDying"]:
                function(relicCard)

def RelicAttack(card, opponent=True):
    player = card.Belonging
    if opponent:
        player = player0 if player == player1 else player1
    numCard = -1
    if [1 for carte in player.Board if carte.Attackable]:
        while 1:
            while numCard < 0 or numCard >= len(player.Board):
                print("Entrer le numero de la carte")
                numCard = int(input())
            if player.Board[numCard].Attackable:
                break
            else:
                print("ERREUR - Carte non attackable")
                numCard = -1
        print(f'Player {card.Belonging.NumPlayer} attack the card {player.Board[numCard].Name} with the relic {card.Name}')
        GetDamaged(player.Board[numCard], card.Belonging, card.Strength)
        GetDamaged(card.Belonging.Board[0], player, player.Board[numCard].Strength)
        Death(player0, player1)
        ModifyDurability(card, 1, opponent=False)
    else:
        print("ERREUR - Aucune cartes attackable")

def Regen(card, amount):
    card.DamageTaken -= amount
    if card.DamageTaken < 0:
        card.DamageTaken = 0
    print(f"La carte {card.Name} regen de {amount}")

def ApplyFunctionToAllCreatures(card, function, *args, conditions, opponent=False):
    player = card.Belonging
    if opponent:
        player = player0 if player == player1 else player1
    for creature in player.Board[1:]:
        if creature conditions: # ------------------------------------------Conditions sous forme de dico ?
            function(card, *args, opponent, specifyCard=creature)




# Card(1, "", , , , {}, property=[], tribu="", description="")

marsh_walker = Card(1, "Marsh Walker", 1, 1, 4, {"OnEndTurn": [lambda self: Regen(self, 1)]}, property=["Regen"], tribu="Wild", description="Regen 1")
shieldbearer = Card(1, "Shieldbearer", 1, 0, 1, {"OnLaying": [lambda self: ModifyStats(self, 1, 1)]}, property=["Roar"], tribu="Olympian", description="Roar : Deal 1 damage")
lowhangingfruit = Card(1, "Low-Hanging Fruit", 1, 0, 0, {"OnLaying": [lambda self: ModifyStats(self, 0, 0, 1, opponent=True, specifyCard=random.choice([enemy for enemy in OpposingPlayer(self.Belonging).Board if enemy.Health <= sorted([i.Health for i in OpposingPlayer(self.Belonging).Board])[0]])), lambda self:Summon(self, vibrant_fruit)]}, property=["Spell"], description="Deal 1 damage to random enemy with least health. Summon 1/1 Vibrant fruit")
vibrant_fruit = Card(0, "Vibrant Fruit", 1, 1, 1, {"OnDying": [lambda self: ModifyStats(self, 1, 1, 0, selfApplicable=True, specifyCard=random.choice([card for card in self.Belonging.Board[1:] if card.Strength >= sorted([i.Strength for i in self.Belonging.Board[1:]])[-1]]) if len(self.Belonging.Board[1:])>0 else None)]}, property=["Afterlife"], description="Give your strongest creature +1/+1")
wild_hog = Card(1, "Wild Hog", 1, 2, 3, {"OnLaying": [lambda self: GetConfused(self)]}, property=["Confused"], tribu="Wild", description="Confused")
vanguard_axewoman = Card(1, "Vanguard Axewoman", 1, 2, 2, {"OnLaying": [lambda self: Blitz(self)]}, property=["Blitz"], tribu="Viking", description="Blitz")
best_friends = Card(1, "Best Friends", 1, 0, 0, {"OnLaying": [lambda self: Summon(self, eagle), lambda self: (Summon(self, badger) if len(self.Belonging.Board)>3 else "")]}, property=["Spell"], description="Summon a confused 2/1 Eagle. Then if you have at least three creatures, summon a confused 1/2 Badger.")
eagle = Card(0, "Eagle", 0, 2, 1, {"OnLaying": [lambda self: GetConfused(self)]}, property=["Confused"], tribu="Wild", description="Confused")
badger = Card(0, "Badger", 0, 1, 2, {"OnLaying": [lambda self: GetConfused(self)]}, property=["Confused"], tribu="Wild", description="Confused")
black_jaguar = Card(1, "Black Jaguar", 2, 3, 3, {"OnLaying": [lambda self: GetConfused(self)], "OnEndTurn": [lambda self: Regen(self, 1)]}, property=["Confused", "Regen"], tribu="Wild", description="Confused, Regen 1")
skeleton_heavy = Card(1, "Skeleton Heavy", 2, 2, 4, {}, property=[], tribu="Anubian", description="")
canopy_barrage = Card(1, "Canopy Barrage", 2, 0, 0, {"OnLaying": [lambda self: ModifyStats(self, 0, 0, 4, opponent=True, specifyCard=random.choice([enemy for enemy in OpposingPlayer(self.Belonging).Board[1:]]) if len(OpposingPlayer(self.Belonging).Board[1:])>0 else None)]}, property=["Spell"], tribu="", description="Deal 4 damage to a random enemy creature")
dune_cavalry = Card(1, "Dune Cavalry", 3, 3, 4, {}, property=[], tribu="", description="")
hunt_warden = Card(1, "Hunt Warden", 3, 3, 4, {}, property=[], tribu="Amazon", description="")
bladefly = Card(1, "Bladefly", 4, 2, 2, {"OnLaying": [lambda self: GetConfused(self), lambda self: Summon(self, bladefly_2), lambda self: Summon(self, bladefly_3)]}, property=["Confused"], tribu="Wild", description="Confused. Roar: Summon 2 Bladeflys")
bladefly_2 = Card(0, "Bladefly", 4, 2, 2, {"OnLaying": [lambda self: GetConfused(self)]}, property=["Confused"], tribu="Wild", description="Confused. Roar: Summon 2 Bladeflys")
bladefly_3 = Card(0, "Bladefly", 4, 2, 2, {"OnLaying": [lambda self: GetConfused(self)]}, property=["Confused"], tribu="Wild", description="Confused. Roar: Summon 2 Bladeflys")
wildfire = Card(1, "Wildfire", 4, 0, 0, {"OnLaying": [lambda self: ApplyFunctionToAllCreatures(self, ModifyStats, 0, 0, 1, opponent=True)]#--------------- a finir -------------------------+[lambda self: ApplyFunctionToAllCreatures(self, ModifyStats, 1, 1, 0, conditions=, opponent=False)]}, property=["Spell"], tribu="", description="Deal 1 damage to each of your opponents creatures. Give +1/+1 and Regen +1 to your wild creatures.")


ToAddInDeck = Card(1, "ToAddInDeck", 0, 1, 1, {})
Impling = Card(1, "Impling", 0, 1, 1, {})
carte_a = Card(1, "a", 1, 2, 2, {"OnEndTurn": [lambda self: Frontline(self)], "OnDying": [lambda self: Frontline(self)]}, property=["Frontline"], description="Frontline")
carte_b = Card(1, "b", 1, 1, 3, {"OnLaying": [lambda self: ModifyStats(self, 0, 0, 1, opponent=True)]}, property=["Roar"], description="Roar : Deal 1 damage")
carte_c = Card(1, "c", 1, 3, 3, {"OnEndTurn": [lambda self: Frontline(self)], "OnDying": [lambda self: Frontline(self)]}, property=["Frontline"], description="Frontline") # verif le OnDying de la frontline
carte_d = Card(1, "d", 1, 2, 4, {"OnEndTurn": [lambda self: Backline(self)], "OnFriendDies": [lambda self: Backline(self)]}, property=["Backline"], description="Backline")
carte_e = Card(1, "e", 1, 3, 1, {"OnDying": [lambda self: Summon(self, Impling)]}, property=["Afterlife"], description="Afterlife : Summon Impling")
carte_f = Card(1, "f", 1, 3, 4, {"OnLaying": [lambda self: ModifyStats(self, 1, 1)]}, property=["Roar"], description="Roar : Add 1/1 to friend")
carte_g = Card(1, "g", 1, 4, 4, {"OnLaying": [lambda self: Blitz(self)]}, property=["Blitz"], description="Blitz")
carte_h = Card(1, "h", 1, 4, 5, {"OnLaying": [lambda self: AddInDeck(self, ToAddInDeck)]}, property=["Roar"], description="Roar : Add card in deck")
carte_i = Card(1, "i", 1, 1, 4, {"OnEnemyDamagedBySelf": [lambda self, opponentCard: ModifyStats(self, -1, 0, 0, opponent=True, specifyCard=opponentCard)]}, description="Remove 1 strength to card damaged by this creature")
carte_j = Card(1, "j", 1, 6, 6, {"OnLaying": [lambda self: GetConfused(self)]}, property=["Confused"], description="Confused")
spell_a = Card(1, "spell_a", 1, 0, 0, {"OnLaying": [lambda self: ModifyStats(self, 0, 0, 2, opponent=True)]}, property=["Spell"], description="Deal 2 damage to a creature")
spell_b = Card(1, "spell_b", 1, 0, 0, {"OnLaying": [lambda self: ModifyStats(self, 0, 0, 3, opponent=True, toCreature=False)]}, property=["Spell"], description="Deal 3 damage to a character")
relic_a = Card(1, "Relic_a", 1, 3, 2, {"OnUse": [lambda self: RelicAttack(self)]}, property=["Relic"])
relic_b = Card(1, "Relic_b", 1, 3, 1, {"OnUse": [lambda self: RelicAttack(self)]}, property=["Relic"])
relic_c = Card(1, "Relic_c", 1, 3, 1, {"OnUse": [lambda self: RelicAttack(self)]}, property=["Relic"])

listCards = [carte_a, carte_b, carte_c, carte_d, carte_e, carte_f, carte_g, carte_h, carte_i, carte_j, ToAddInDeck, Impling, spell_a, spell_b, relic_a, relic_b, relic_c]
pub0 = Publisher(listEvents)
pub1 = Publisher(listEvents)
global player0, player1, game
# player0 = Player(0, True, deck = [carte_a, carte_c, carte_e, carte_g, carte_i, spell_a, relic_a, relic_c], publisher=pub0)
# player1 = Player(1, False, deck = [carte_b, carte_d, carte_f, carte_h, carte_j, spell_b, relic_b, marsh_walker], publisher=pub1)
player0 = Player(0, True, deck = [black_jaguar, canopy_barrage, best_friends, marsh_walker, shieldbearer], publisher=pub0)
player1 = Player(1, False, deck = [skeleton_heavy, wildfire, carte_f, lowhangingfruit], publisher=pub1)

game = Game()
game.Start(player0, player1)



# player0.ShowPlayer()
# player1.ShowPlayer()
#
# player0.UseTricks(game)
# player1.UseTricks(game)
#
# player0.LayCard(1)
# player1.LayCard(0)
#
# player0.AttackWithCard(player1, 1, 0)
# player1.AttackWithCard(player0, 1, 1)
#
# player0.EndTurn(player1, game)
# player1.EndTurn(player0, game)





# TODO dieu confused, relic tappent ramdom ??
# TODo est ce que si une carte a -1 strength on attack et attaque le dieu, elle lui retir 1 a sa relic ?

    # TODO rechercher combien d'exemplaire d'une carte on peut mettre par Deck en ft de la rareté

    # TODO favors


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























