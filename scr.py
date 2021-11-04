from flask import Flask, request, jsonify

app = Flask(__name__)


@app.get("/hello")
def get_countries():
    return 'helllo py'