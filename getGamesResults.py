import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def run(url, date):
    try:
        scraper = cloudscraper.create_scraper()
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://stats.ncaa.org/",  
        }

        scraper.get(url, headers=headers)

        r = scraper.get(url, headers=headers)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.find_all(class_="card m-2")

        for card in cards:
            teams = [t.get_text(strip=True) for t in card.find_all(class_="opponents_min_width")] # winner will have class winner background, check if this matters
            scores = [s.get_text(strip=True) for s in card.find_all(class_="p-1")] # div class = "p-1"
            return format_game(date, teams[0], teams[1], scores[0], scores[1])
            
            
    except Exception as e:
        print(f"error: {e}")



def format_game(game_date, team1, team2, team1_score, team2_score):
    return {
        "date": game_date,
        "team1": team1,
        "team2": team2,
        "team1score": team1_score,
        "team2score": team2_score
    }


def getGames():
    today = datetime.now()
    date = today - timedelta(days=114)

    month_str = str(date.month).zfill(2)
    day_str = str(date.day).zfill(2)
    year_str = str(date.year)

    url = (
        f"https://stats.ncaa.org/season_divisions/18484/livestream_scoreboards"
        f"?utf8=%E2%9C%93&season_division_id=&game_date={month_str}%2F{day_str}%2F{year_str}"
        f"&conference_id=0&tournament_id=&commit=Submit"
    )
    run(url, today)

getGames()
