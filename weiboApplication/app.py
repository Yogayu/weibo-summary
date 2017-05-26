from flask import Flask, url_for, request
from flask import render_template, json

app = Flask(__name__)

# def main():
    # return render_template('index.html')

@app.route("/")
def index():
    return render_template('index2.html')

@app.route("/algorithm")
def algorithm():
    return render_template('index.html')

@app.route('/hello')
def helloagain():
    return 'Nice to meet you.'

if __name__ == "__main__":
    app.run()