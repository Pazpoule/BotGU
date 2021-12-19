from tkinter import *
from game import *

def ShowPlayer(fenetre, numPlayer):
    for player in [player0, player1]:
        if numPlayer == player.NumPlayer:
            player.ShowPlayer()
    fenetre.destroy()
    createWindow()

def EndTurn(fenetre, numPlayer):
    for player in [player0, player1]:
        if numPlayer == player.NumPlayer:
            player.EndTurn([p for p in [player0, player1] if p!=player][0], game)
    fenetre.destroy()
    createWindow()

def UseTrick(fenetre, numPlayer):
    for player in [player0, player1]:
        if numPlayer == player.NumPlayer:
            player.UseTricks()
    fenetre.destroy()
    createWindow()

def LayCard(fenetre, numPlayer, num):
    for player in [player0, player1]:
        if numPlayer == player.NumPlayer:
            player.LayCard(num)
    fenetre.destroy()
    createWindow()

def Attack(fenetre, numPlayer, numCard, numCardDef):
    for player in [player0, player1]:
        if numPlayer == player.NumPlayer:
            otherPlayer = [p for p in [player0, player1] if p!=player][0]
            player.AttackWithCard(otherPlayer, numCard, numCardDef)
    fenetre.destroy()
    createWindow()

def UseAbility(fenetre, numPlayer, numCard=None, relic=False):
    for player in [player0, player1]:
        if numPlayer == player.NumPlayer:
            if relic:
                player.UseAbility(relic=True)
            else:
                player.UseAbility(numCardOnBoard=numCard)
    fenetre.destroy()
    createWindow()


def createWindow():
    fenetre = Tk()
    fenetre.title("GU")
    fenetre.geometry('1200x800+700+100')
    fenetre['bg']='white'

    for player in [player0, player1]:
        if player==player0:
            position=0
        else:
            position=1
        Frame_player = Frame(fenetre, borderwidth=2, relief=GROOVE)
        Frame_player.grid(row=0, column=position, padx=10, pady=10)
        Label(Frame_player, text="Player "+str(player.NumPlayer)).grid(row=0, column=0)
        Label(Frame_player, text="Health :     ").grid(row=1, column=0)
        Label(Frame_player, text=player.Board[0].Health).grid(row=1, column=1)
        Label(Frame_player, text="Mana Dispo : ").grid(row=2, column=0)
        Label(Frame_player, text=player.ManaDispo).grid(row=2, column=1)
        Label(Frame_player, text="Frenzied : ").grid(row=3, column=0)
        Label(Frame_player, text=player.Frenzied).grid(row=3, column=1)
        Label(Frame_player, text="Relic : ").grid(row=4, column=0)
        Label(Frame_player, text=player.Relic.Name).grid(row=4, column=1) if player.Relic != None else ""
        # Hand
        Label(Frame_player, text="Hand :       ").grid(row=5, column=0)
        Frame_player_Hand = Frame(Frame_player, borderwidth=2, relief=GROOVE)
        Frame_player_Hand.grid(row=6, column=0)
        Label(Frame_player_Hand, text="Name :  ").grid(row=0, column=0)
        Label(Frame_player_Hand, text="Mana :  ").grid(row=1, column=0)
        Label(Frame_player_Hand, text="Strength :").grid(row=2, column=0)
        Label(Frame_player_Hand, text="Health :").grid(row=3, column=0)
        for numCard, card in enumerate(player.Hand):
            Label(Frame_player_Hand, text=card.Name).grid(row=0, column=1+numCard)
            Label(Frame_player_Hand, text=card.Mana).grid(row=1, column=1+numCard)
            Label(Frame_player_Hand, text=card.Strength).grid(row=2, column=1+numCard) if "Spell" not in card.Property else ""
            Label(Frame_player_Hand, text=card.Health).grid(row=3, column=1+numCard) if "Spell" not in card.Property else ""
        # Board
        Label(Frame_player, text="Board :       ").grid(row=5, column=1)
        Frame_player_Board = Frame(Frame_player, borderwidth=2, relief=GROOVE)
        Frame_player_Board.grid(row=6, column=1)
        Label(Frame_player_Board, text="Name :  ").grid(row=0, column=0)
        Label(Frame_player_Board, text="Mana :  ").grid(row=1, column=0)
        Label(Frame_player_Board, text="Strength :").grid(row=2, column=0)
        Label(Frame_player_Board, text="Health :").grid(row=3, column=0)
        for numCard, card in enumerate(player.Board[1:]):
            Label(Frame_player_Board, text=card.Name, bg="aquamarine" if card.Ready else "pink").grid(row=0, column=1+numCard)
            Label(Frame_player_Board, text=card.Mana).grid(row=1, column=1+numCard)
            Label(Frame_player_Board, text=card.Strength).grid(row=2, column=1+numCard) if "Spell" not in card.Property else ""
            Label(Frame_player_Board, text=card.Health).grid(row=3, column=1+numCard) if "Spell" not in card.Property else ""
        # Tricks
        Label(Frame_player, text="Tricks :").grid(row=12, column=0)
        Label(Frame_player, text=player.Tricks).grid(row=12, column=1)
        # Turn
        Label(Frame_player, text="Turn :").grid(row=13, column=0)
        Label(Frame_player, text=player.Turn, bg=player.Turn*"green" + (1-player.Turn)*"red").grid(row=13, column=1)

    # Pannel des actions possibles
    Frame_actions = Frame(fenetre, borderwidth=2, relief=GROOVE)
    Frame_actions.grid(row=1, column=0, padx=10, pady=10)
    player = player0 if player0.Turn else player1
    numPlayer = player.NumPlayer
    listActions = []
    action = 0
    listActions.append(Button(Frame_actions, text="End Turn", command=lambda: EndTurn(fenetre, numPlayer)))
    listActions[action].grid(row=action, column=0)
    action += 1
    for numCarte, carte in enumerate(player.Hand):
        listActions.append(Button(Frame_actions, text=f'Lay card {carte.Name}', command=lambda numCarte=numCarte: LayCard(fenetre, numPlayer, numCarte)))
        listActions[action].grid(row=action, column=0)
        action += 1
    for numCard, card in enumerate(player.Board):
        if card.Ready:
            for numCardDef, cardDef in enumerate([p for p in [player0, player1] if p!=player][0].Board):
                if cardDef.Attackable and not (card.CanAttackGod==False and cardDef.Name=="GOD"):
                    listActions.append(Button(Frame_actions, text=f'Card {card.Name} attack {cardDef.Name}', command=lambda numCard=numCard, numCardDef=numCardDef: Attack(fenetre, numPlayer, numCard, numCardDef)))
                    listActions[action].grid(row=action, column=0)
                    action += 1
    for numCard, card in enumerate(player.Board):
        if "Ability" in card.Property and card.Ready:
            listActions.append(Button(Frame_actions, text="Use "+card.Name+" Ability", command=lambda: UseAbility(fenetre, numPlayer, numCard)))
            listActions[action].grid(row=action, column=0)
            action += 1
    if player.Relic != None:
        if player.Relic.Ready:
            listActions.append(Button(Frame_actions, text="Use Relic "+player.Relic.Name, command=lambda: UseAbility(fenetre, numPlayer, relic=True)))
            listActions[action].grid(row=action, column=0)
            action += 1
    listActions.append(Button(Frame_actions, text="Use Trick", command=lambda: UseTrick(fenetre, numPlayer)))
    listActions[action].grid(row=action, column=0)
    action += 1



    # Affichage Carte
    Frame_cartes = Frame(fenetre, borderwidth=2, relief=GROOVE)
    Frame_cartes.grid(row=1, column=1, padx=10, pady=10)
    Label(Frame_cartes, text="Name", bg="white").grid(row=0, column=0)
    Label(Frame_cartes, text="Mana", bg="white").grid(row=0, column=1)
    Label(Frame_cartes, text="Strength", bg="white").grid(row=0, column=2)
    Label(Frame_cartes, text="Health", bg="white").grid(row=0, column=3)
    Label(Frame_cartes, text="Description", bg="white").grid(row=0, column=4)
    for i, card in enumerate(listCards):
        i += 1
        background = "aliceblue" if i%2==0 else "whitesmoke"
        Label(Frame_cartes, text=card.Name, bg=background).grid(row=i, column=0)
        Label(Frame_cartes, text=card.Mana, bg=background).grid(row=i, column=1)
        Label(Frame_cartes, text=card.Strength, bg=background).grid(row=i, column=2)
        Label(Frame_cartes, text=card.Health, bg=background).grid(row=i, column=3)
        Label(Frame_cartes, text=card.Description, bg=background).grid(row=i, column=4)

    fenetre.mainloop()

createWindow()













