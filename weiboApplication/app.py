from flask import Flask, url_for, request
from flask import render_template, json

app = Flask(__name__)

# def main():
    # return render_template('index.html')

@app.route("/")
def index():
    # return url_for('static', filename='css/style.css')
    return render_template('index.html')

@app.route("/algorithm")
def algorithm():
    # return render_template('index2.html')
    return render_template('test.html')

@app.route('/summary')
def helloagain():
    return render_template('test.html')

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == "__main__":
    app.run()