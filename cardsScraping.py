from time import sleep
from datetime import date, timedelta
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

if __name__ == '__main__':


    link = "https://gudecks.com/meta/card-rankings?timeFrame=30&userRank=4&decksWithCard=5000"

    # On crée une instance du web-driver Firefox
    driver = webdriver.Firefox()
    # On positionne la fenêtre a droite
    driver.set_window_position(700, 50, windowHandle='current')
    # On se connecte sur la page
    driver.get(link)
    # On renseigne les ID quand la page est chargé (ie quand on peut trouver le champs sans generer une erreur)
    dataCards = pd.DataFrame({"Names": [], "Gods": [], "Sets": [],"Matches": [], "Percent_of_decks": [], "Copies": [], "Win_rates": [], "Unique_win_rates": [], "Prices": []})
    for _ in range(17):
        montre = 0
        while montre == 0:
            try:
                driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/div[2]").text
                montre = 1
            except:
                print("En cours...")
        datatmp = pd.DataFrame({})
        names=[]
        gods = []
        sets = []
        matches = []
        percentOfDecks = []
        copies = []
        winRates = []
        uniqueWinRates = []
        prices = []
        for row in range(2, 21):
            try:
                names.append(driver.find_element(By.XPATH,          f"/ html / body / div[1] / div[1] / div / div[2] / div[1] / div[2] / div[1] / div[2] / div[{row}] / div / div[1] / div / div[2]").text)
                gods.append(driver.find_element(By.XPATH,           f"/ html / body / div[1] / div[1] / div / div[2] / div[1] / div[2] / div[1] / div[2] / div[{row}] / div / div[2]").text)
                sets.append(driver.find_element(By.XPATH,           f"/ html / body / div[1] / div[1] / div / div[2] / div[1] / div[2] / div[1] / div[2] / div[{row}] / div / div[3]").text)
                matches.append(driver.find_element(By.XPATH,        f"/ html / body / div[1] / div[1] / div / div[2] / div[1] / div[2] / div[1] / div[2] / div[{row}] / div / div[4] / div").text)
                percentOfDecks.append(driver.find_element(By.XPATH, f"/ html / body / div[1] / div[1] / div / div[2] / div[1] / div[2] / div[1] / div[2] / div[{row}] / div / div[5]").text)
                copies.append(driver.find_element(By.XPATH,          f"/ html / body / div[1] / div[1] / div / div[2] / div[1] / div[2] / div[1] / div[2] / div[{row}] / div / div[6]").text)
                winRates.append(driver.find_element(By.XPATH,       f"/ html / body / div[1] / div[1] / div / div[2] / div[1] / div[2] / div[1] / div[2] / div[{row}] / div / div[7] / div").text)
                uniqueWinRates.append(driver.find_element(By.XPATH, f"/ html / body / div[1] / div[1] / div / div[2] / div[1] / div[2] / div[1] / div[2] / div[{row}] / div / div[8] / div").text)
                prices.append(driver.find_element(By.XPATH,         f"/ html / body / div[1] / div[1] / div / div[2] / div[1] / div[2] / div[1] / div[2] / div[{row}] / div / div[9] / div").text)
            except:
                print("Fin de page")
                break
        datatmp["Names"] = names
        datatmp["Gods"] = gods
        datatmp["Sets"] = sets
        datatmp["Matches"] = matches
        datatmp["Percent_of_decks"] = percentOfDecks
        datatmp["Copies"] = copies
        datatmp["Win_rates"] = winRates
        datatmp["Unique_win_rates"] = uniqueWinRates
        datatmp["Prices"] = prices

        dataCards = dataCards.append(datatmp)
        dataCards.reset_index(inplace=True, drop=True)
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[2]/div/div[3]/button").click()
        except:
            print("Derniere page")
            break
        sleep(2)
    # On transforme les donnée en float
    dataCards["Prices"] = dataCards["Prices"].astype("float")
    for row in range(len(dataCards)):
        dataCards.loc[row, "Win_rates"] = float(dataCards.loc[row, "Win_rates"][:-1])
    # On créer l'indicateur
    dataCards["Rate"] = dataCards["Prices"] / dataCards["Win_rates"]
    # On trie par l'indicateur
    dataCards.sort_values(by="Rate", ascending=True, inplace=True)

    dataCardsSelect = dataCards[(dataCards["Win_rates"]>=60) & (dataCards["Prices"]>0)]










    linkdecks = "https://gudecks.com/meta/top-decks?userRank=4"


    # On crée une instance du web-driver Firefox
    driver = webdriver.Firefox()
    # On positionne la fenêtre a droite
    driver.set_window_position(700, 50, windowHandle='current')
    # On se connecte sur la page
    driver.get(linkdecks)
    # On renseigne les ID quand la page est chargé (ie quand on peut trouver le champs sans generer une erreur)
    dataDecks = pd.DataFrame({"Names": [], "By": [], "Win_rates": [], "Prices": []})

    montre = 0
    while montre == 0:
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[1]/div/div[2]/a/div").text
            montre = 1
        except:
            print("En cours...")
    for _ in range(5):
        datatmp = pd.DataFrame({})
        names=[]
        by = []
        winRates = []
        prices = []
        for row in range(1, 21):
            try:
                names.append(driver.find_element(By.XPATH,      f"/ html / body / div[1] / div[1] / div / div[2] / div / div[2] / div[2] / div[1] / div[2] / div[{row}] / div / div[1] / div / div[2] / a / div").text)
                by.append(driver.find_element(By.XPATH,         f"/ html / body / div[1] / div[1] / div / div[2] / div / div[2] / div[2] / div[1] / div[2] / div[{row}] / div / div[1] / div / div[2] / div / a").text)
                winRates.append(driver.find_element(By.XPATH,   f"/ html / body / div[1] / div[1] / div / div[2] / div / div[2] / div[2] / div[1] / div[2] / div[{row}] / div / div[2] / div / div[1]").text)
                prices.append(driver.find_element(By.XPATH,     f"/ html / body / div[1] / div[1] / div / div[2] / div / div[2] / div[2] / div[1] / div[2] / div[{row}] / div / div[8] / div").text)
            except:
                print("Fin de page")
                break
        datatmp["Names"] = names
        datatmp["By"] = by
        datatmp["Win_rates"] = winRates
        datatmp["Prices"] = prices

        dataDecks = dataDecks.append(datatmp)
        dataDecks.reset_index(inplace=True, drop=True)
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div[2]/div[2]/div[2]/div/div[3]/button").click()
        except:
            print("Derniere page")
            break
        sleep(1)

    # On transforme les donnée en float
    dataDecks["Prices"] = dataDecks["Prices"].astype("float")
    for row in range(len(dataDecks)):
        dataDecks.loc[row, "Win_rates"] = float(dataDecks.loc[row, "Win_rates"][:-1])

    # On créer l'indicateur
    dataDecks["Rate"] = dataDecks["Prices"] / dataDecks["Win_rates"]
    # On trie par l'indicateur
    dataDecks.sort_values(by="Rate", ascending=True, inplace=True)

    dataDecksSelect = dataDecks[(dataDecks["Win_rates"]>=80) & (dataDecks["Prices"]>0)]












