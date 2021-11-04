import time
from threading import Thread
from flask import Flask, request, jsonify

app = Flask(__name__)

soccerRankingTable = 'bla-'


@app.get("/hello")
def get_countries():
    return soccerRankingTable


def loadSoccerRankingTable(name):
    global soccerRankingTable
    while True:
        print(f"Thread {name}: starting")
        soccerRankingTable = soccerRankingTable + soccerRankingTable
        time.sleep(5)


if __name__ == '__main__':
    readSoccerTableThread = Thread(target=loadSoccerRankingTable, args=(1,))
    readSoccerTableThread.start()

    app.config['JSON_AS_ASCII'] = False
    port= 5000
    runFlaskThread = Thread(target=app.run, args=('0.0.0.0', port, False))
    runFlaskThread.start()
