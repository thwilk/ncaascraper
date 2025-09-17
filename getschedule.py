from bs4 import BeautifulSoup
import pandas as pd 
import requests
import datetime


date = datetime.datetime.now()
date = date.strftime("%y/%m/%d")
print(date)
url = f"https://www.ncaa.com/scoreboard/lacrosse-men/d1/20{date}/all-conf"


def run():
    try:
        r = requests.get(url)
        print(url)    
        games = []
        soup = BeautifulSoup(r.text, 'html.parser')
        soup = soup.find_all(class_="gamePod-game-team-name")
        for x in range(0, len(soup)//2):
            t = x*2
            games.append([soup[t].text, soup[t+1].text])
        

        print("TODAYS GAMES ARE:\n--------------------------\n")
        for game in games:
            print(f"{game[0]} @\n{game[1]}\n")
        
    
    
    except Exception as e:
        print("Whoes a good little boy?!?!?!??!?!?!")
        print(e)

run()