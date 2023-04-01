import time

from threading import Thread
from flask import Flask, render_template, request
from fileinput import filename

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/success', methods=['POST'])
def success():
    from alert import sendAlert
    from vidProcess import processVid
    if request.method == 'POST':
        f = request.files['vid']
        n = f.filename.split(".")
        newName = "sample."+n[len(n)-1]
        f.save(newName)
        accFound = False
        accFound = processVid(accFound, newName)
        if accFound:
            alert_thread = Thread(target=sendAlert)
            alert_thread.start()
            return render_template("result.html")
        else:
            print("No Accident")
            return render_template("index.html")
