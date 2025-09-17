import urldict
import datetime
import template as t
import os
import pandas as pd


# this script will combine all saved stats 
def makeChart(d:str):
    directory_path = f"/Users/tommywilk/Desktop/personal projects/ncaascraper/stats/{d}/team/"
    df = pd.read_csv("/Users/tommywilk/Desktop/personal projects/ncaascraper/stats/alphabetical.csv")
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            try:
                #print (file_path)
                temp = pd.read_csv(file_path)
                #df = pd.merge(df, temp, on="Team", how="outer", suffixes=("queer", "faggot"))
                print(temp.columns[-1])
                df = pd.merge(df, temp[['Team', temp.columns[-1]]], on='Team', how='left')

            except Exception as e:
                print(e)
        
    df.drop(df.columns[0], axis = 1, inplace=True)
    df =df.sort_values(by='Team')


    return df
        


# this method will download all stats from the website and save them
def downloadstats():
    scraper = t.Template(urldict.individualStatUrls, urldict.individualStatUrlsPageNums, "individual")
    scraper.printStats()
    scraper = t.Template(urldict.teamStatUrls, urldict.teamStatUrlPageNums, "team")
    scraper.printStats()
    scraper = t.Template(urldict.RPI, urldict.RPIpages, "team")
    scraper.printStats()

if __name__ == "__main__":   
    downloadstats()
    date = datetime.datetime.now().strftime("%x").replace("/","_")
    x=makeChart(date)
    x.to_csv(f'/Users/tommywilk/Desktop/personal projects/ncaascraper/stats/{date}/stats.csv')

