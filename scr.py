import time, json
from bs4 import BeautifulSoup
import urllib3
import re
from threading import Thread
from flask import Flask, request, jsonify

app = Flask(__name__)

soccerRankingTable = {"clubs":[
        {
            "club_short" : "FCB",
            "club_full" : "FC Bayern München",
            "ranking" : "1"
        },
        {
            "club_short" : "BVB",
            "club_full" : "Borussia Dortmund",
            "ranking" : "6"
        },
        {
            "club_short" : "VFL",
            "club_full" : "VFL Bochum",
            "ranking" : "8"
        },
        {
            "club_short" : "S04",
            "club_full" : "FC Schalke 04",
            "ranking" : "3"
        }
]}

@app.get("/clubs")
def getAvailableSoccerClubs():
    allClubs = {'clubs':[]}
    for soccerClub in soccerRankingTable['clubs']:
        del soccerClub['ranking']
        allClubs['clubs'].append(soccerClub)
    return json.dumps(allClubs)


@app.get("/ranking/<club>")
def getRankgingForClub(club=None):
    ranking='0'
    for clubRanking in soccerRankingTable['clubs']:
        if(clubRanking['club_short'] == club):
            ranking = clubRanking['ranking']
            break

    return ranking

def loopForRankingLoader():
    global soccerRankingTable
    while True:
        try:
            loadSoccerRankingTable()
        except:
            pass
        time.sleep(10*60)

def loadSoccerRankingTable():
    global soccerRankingTable
    
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"

    print('open URL')
    http = urllib3.PoolManager()
    url = 'https://www.bundesliga.com/de/2bundesliga/tabelle'
    html = http.request('GET', url)

    print('doing soap stuff')
    soup = BeautifulSoup(html, features="html.parser")
    ##for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
    print(soup.findAll('html'))
    for link in soup.findAll('a'):
        print(link.get('href'))

    ##print(html)
    f = open("tabelle.html", "a")
    f.write(html.data.decode('utf-8'))
    f.close()
    print('written')


if __name__ == '__main__':
    loadSoccerRankingTable()
    
    readSoccerTableThread = Thread(target=loopForRankingLoader, args=())
    #readSoccerTableThread.start()

    app.config['JSON_AS_ASCII'] = False
    port= 5000
    runFlaskThread = Thread(target=app.run, args=('0.0.0.0', port, False))
    ##runFlaskThread.start()
