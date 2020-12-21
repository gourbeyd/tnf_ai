#!/bin/env python3
import subprocess
import selenium
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import date
import sqlite3
conn = sqlite3.connect("tnf.bd")
matchs = conn.cursor()
today = date.today().strftime("%Y-%m-%d")

def double_chance(c1, c2):
    m1=c2/(c1+c2)
    return round(m1*c1, 2)

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
#driver.get("http://google.com")
pages = []

pages.append("https://www.flashscore.fr/football/angleterre/premier-league/")
pages.append("https://www.flashscore.fr/football/allemagne/bundesliga/")
pages.append("https://www.flashscore.fr/football/france/ligue-1/")
pages.append("https://www.flashscore.fr/football/espagne/laliga/")
pages.append("https://www.flashscore.fr/football/italie/serie-a/")
liste_url_matchs = []
for page in pages:
    browser = webdriver.Firefox(options=options)
    browser.get(page)
    tab=browser.find_element_by_class_name("event--live").find_elements_by_class_name('event__match--scheduled')
    for elem in tab:
        liste_url_matchs.append(elem.get_attribute("id")[4:])
    browser.quit()
print(len(liste_url_matchs), "matchs le ", today)
for k in range(len(liste_url_matchs)):
    page = "https://www.flashscore.fr/match/"+liste_url_matchs[k]+"/#resume-du-match"
    browser = webdriver.Firefox(options=options)
    browser.get(page)
    #html = browser.page_source
    scraped_odds = browser.find_elements_by_class_name("odds.value")
    home_team = browser.find_element_by_class_name("team-text.tname-home").text
    away_team = browser.find_element_by_class_name("team-text.tname-away").text
    cotes = []
    for element in scraped_odds[3:6]:
        cotes.append(float(element.text))
    page_dom = "https://www.flashscore.fr/match/"+liste_url_matchs[k]+"/#classement"
    browser.close()
    browser = webdriver.Firefox(options=options)
    browser.get(page_dom)
    html = browser.page_source
    #print(html)
    #print(cotes)
    tableau_dom = browser.find_element_by_class_name("rows___1BdItrT").text
    compteur = 0
    to_iter_classement = tableau_dom.splitlines()
    for mot in to_iter_classement:
        #print(mot)
        if mot == home_team:
            pshg=int(to_iter_classement[compteur+5].split(sep=":")[0])
            buts =pshg
        compteur+=1
    browser.close()
    #print(buts)
    page_ext = "https://www.flashscore.fr/match/"+liste_url_matchs[k]+"/#classement"
    browser = webdriver.Firefox(options=options)
    browser.get(page_ext)
    html = browser.page_source
    #print(html)
    tableau_ext = browser.find_element_by_id("tab-match-standings").text
    compteur = 0
    to_iter_classement = tableau_ext.splitlines()
    for mot in to_iter_classement:
        #print(mot)
        if mot == away_team:
            buts -= int(to_iter_classement[compteur+5].split(sep=":")[0])
            psag=int(to_iter_classement[compteur+5].split(sep=":")[0])
        compteur+=1
    #print(buts)
    browser.close()
    print(home_team + " vs " + away_team)
    cotes.append(buts)
    if len(cotes) > 1:
        subprocess.call(['./bundes.py', str(cotes[0]), str(cotes[1]), str(cotes[2]), str(cotes[3]), liste_url_matchs[k]])
        matchs.execute("""INSERT INTO MATCHS(id, date, HomeTeam, AwayTeam, ODD_HOME, ODD_DRAW, ODD_AWAY, OD_DRAW_OR_AWAY, PSHG, PSAG) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (liste_url_matchs[k], today, home_team, away_team, cotes[0], cotes[1], cotes[2], double_chance(cotes[1], cotes[2]), int(pshg), int(psag)))
        conn.commit()
        
    #else:
     #   break
    #print(tableau_dom) 
conn.close()
