import time, json
from threading import Thread
from flask import Flask, request, jsonify

app = Flask(__name__)

soccerRankingTable = {
    "league1" : [
        {
            "club" : "FCB",
            "ranking" : "1"
        },
        {
            "club" : "BVB",
            "ranking" : "6"
        }
    ],
    "league2" : [
        {
            "club" : "S04",
            "ranking" : "3"
        },
        {
            "club" : "Bielefeld",
            "ranking" : "8"
        }
    ]
}


@app.get("/ranking/<club>")
def getRankgingForClub(club=None):
    ranking='0'
    for clubRanking in soccerRankingTable['league1']:
        if(clubRanking['club'] == club):
            ranking = clubRanking['ranking']
            break

    for clubRanking in soccerRankingTable['league2']:
        if(clubRanking['club'] == club):
            ranking = clubRanking['ranking']
            break

    return ranking


def loadSoccerRankingTable():
    global soccerRankingTable
    while True:
        soccerRankingTable = soccerRankingTable + soccerRankingTable
        time.sleep(5)


if __name__ == '__main__':
    readSoccerTableThread = Thread(target=loadSoccerRankingTable, args=(1,))
    readSoccerTableThread.start()

    app.config['JSON_AS_ASCII'] = False
    port= 5000
    runFlaskThread = Thread(target=app.run, args=('0.0.0.0', port, False))
    runFlaskThread.start()
