from flask import Flask, send_from_directory
import data

app = Flask(__name__)

@app.route('/')
def getHTML():
    return send_from_directory('.', 'page.html')

@app.route('/script.js')
def getScript():
    return send_from_directory('.', 'script.js')

@app.route('/ajax.js')
def getAjax():
    return send_from_directory('.', 'ajax.js')

@app.route('/data')
def getData():
    dataJSON = data.betterJSONDic(14)
    return dataJSON

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
