import time, json
from bs4 import BeautifulSoup
import urllib3
import re
from threading import Thread
from flask import Flask, request, jsonify

app = Flask(__name__)

urlBL1 = 'https://www.bundesliga.com/de/bundesliga/tabelle'
urlBL2 = 'https://www.bundesliga.com/de/2bundesliga/tabelle'

appInfo = {"info":[]}

## TODO save the initial club list in a settings.json
soccerRankingTable = {"clubs":[
        {
            "club_short" : "FCB",
        },
        {
            "club_short" : "BVB",
        },
        {
            "club_short" : "BOC",
        },
        {
            "club_short" : "S04",
        }
]}

@app.route("/info")
def getInformation():
    return appInfo

@app.route("/clubs")
def getAvailableSoccerClubs():
    allClubs = {'clubs':[]}
    for soccerClub in soccerRankingTable['clubs']:
        allClubs['clubs'].append(soccerClub)
    return json.dumps(allClubs)


@app.route("/ranking/<clubShort>")
def getRankgingForClub(clubShort=None):
    ranking='0'
    try: 
        for clubRanking in soccerRankingTable['clubs']:
            if(clubRanking['club_short'] == clubShort):
                ranking = clubRanking['rank']
                break
    except:
        pass
    return ranking

def loopForRankingLoader(delay):
    global soccerRankingTable
    while True:
        try:
            loadSoccerRankingTable(urlBL1)
            loadSoccerRankingTable(urlBL2)
        except:
            print(f'error while reading ranking from {urlBL1} or {urlBL2}')
            pass

        print(f'waiting for {delay} minutes before reading the rankings again')
        time.sleep(60 * delay)

def loadSoccerRankingTable(url):
    global soccerRankingTable
    print(f'read ranking from {url}')
    http = urllib3.PoolManager()
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
    html = http.request('GET', url, headers=headers)

    htmlFull = BeautifulSoup(html.data.decode('utf-8'), features="html.parser")

    for htmlRow in htmlFull.findAll('tr', attrs={'class': re.compile("^table-DFL-")}):
        curClubLong,curClubShort,curRank = '','',''
        for htmlCol in htmlRow.findChildren('td'):
            if(htmlCol.get('class')[0] == 'rank'):
                curRank = htmlCol.text
            if(htmlCol.get('class')[0] == 'team'):
                curClubLong = htmlCol.findChildren('div')[0].get('title')
                curClubShort = htmlCol.findChildren('div')[0].findChildren('span')[0].text

        saveCurrentRanking(curClubShort, curClubLong, curRank)


def saveCurrentRanking(clubShort, clubLong, rank):
    global appInfo
    #print(f'{rank} # {clubLong} ({clubShort})')
    appInfo['info'].append("{ 'rank' : '" + rank + "', " + 
                            "'club_long' : '" + clubLong + "', " + 
                            "'club_short' : '" + clubShort + "'}")
    for clubRanking in soccerRankingTable['clubs']:
        if(clubRanking['club_short'] == clubShort):
            clubRanking['club_long'] = clubLong
            clubRanking['rank'] = rank


if __name__ == '__main__':
    delayForRankingLoopingInMinutes = 120
    readSoccerTableThread = Thread(target=loopForRankingLoader, args=(delayForRankingLoopingInMinutes,))
    readSoccerTableThread.start()

    app.config['JSON_AS_ASCII'] = False
    port= 5000
    runFlaskThread = Thread(target=app.run, args=('0.0.0.0', port, False))
    runFlaskThread.start()
