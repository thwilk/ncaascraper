import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
import datetime
import os as os 


class Template:
    def __init__(self, urls:list, pages: list, type:str):
        print("lol")
        if not (type == "team" or type == "individual" or type == "teamsheet"):
            raise Exception("Type parameter must be 'team' or 'individual', representing type of stat")
        if not (len(urls)==len(pages)):
            raise Exception("Url's and Pages length doesnt match.")
        self.pages = pages
        self.urls = urls
        self.type = type
        self.currentName = ""
    


    def getStats(self, base_url):
        try:

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Referer": "https://www.google.com/",
            }

            r = requests.get(base_url, headers=headers)
            print(f"Retrieving from {base_url}")
            print(f"response: {r.status_code}\n")


            soup = BeautifulSoup(r.text, 'html.parser')
            stats_table = soup.find("table")
            try:
                self.currentName = soup.find(class_="stats-header__lower__title").text.strip()
            except Exception as e:
                pass
            if not self.currentName:
                self.currentName = "RPI"

            headers = [header.text.strip() for header in stats_table.find_all('th')]
            headers[-1] = self.currentName.replace(" ", "").replace("-","")
            rows = []
            for row in stats_table.find_all('tr')[1:]:  # skip the header row
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    rows.append(cols)
            
            return headers, rows

        except requests.HTTPError as e:
            print(f'HTTP Error occurred: {e.response.status_code}')
            return None, None
        except requests.RequestException as e:
            print(f'Request exception: {e}')
            return None, None
        except Exception as e:
            print(f'An error occurred: {e}')
            return None, None

    def printStats(self):
        #each page
        for x in range(0, len(self.urls)):
            all_rows = []
            all_headers = None

            # data from each page
            for page in range(1,self.pages[x]+1):
                if page >1:
                    url = self.urls[x] + "/p"+str(page)
                else:
                    url = self.urls[x]
                headers, rows = self.getStats(url)
                
                if headers and rows:
                    all_headers = headers  
                    all_rows.extend(rows)  

            if all_headers and all_rows:
                df = pd.DataFrame(all_rows, columns=all_headers)
                
                # to csv
                self.currentName=self.currentName.replace(" ","_")
                x = datetime.datetime.now().strftime("%x").replace("/","_")
                try:
                    try: 
                        os.mkdir(f"/Users/tommywilk/Desktop/personal projects/ncaascraper/stats/{x}")
                    except FileExistsError as e:
                        pass
                    except Exception as e:
                        print("IM RETARDED")
                        
                    os.mkdir(f"/Users/tommywilk/Desktop/personal projects/ncaascraper/stats/{x}/{self.type}")
                except FileExistsError as e:
                    pass
                except Exception as e:
                    print(e)
                df.to_csv(f'/Users/tommywilk/Desktop/personal projects/ncaascraper/stats/{x}/{self.type}/{self.currentName}{x}.csv', index=False)
                print(f"Data saved to stats/{x}/{self.type}/{self.currentName}{x}.csv")
        
print("")



"""
HOW TO USE: 
create list of urls from stats from ncaa.com/stats,
create a list of how many pages corresponding to that stat,
create template class with these to lists
then use x.printStats() to save it

"""
