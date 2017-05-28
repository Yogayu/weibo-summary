#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
import os
import os.path as op

from flask import Flask, url_for, request, redirect
from flask import render_template, json, session
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.event import listens_for
from jinja2 import Markup

from flask_admin import Admin, form
from flask_admin.form import rules
from flask_admin.contrib import sqla
from flask_admin.contrib.fileadmin import FileAdmin

# languages
from flask_babelex import Babel

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:youxinyu@localhost:3306/weibodb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# set flask admin swatch
app.config['FLASK_ADMIN_SWATCH'] = 'Flatly'

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

@app.route("/")
def index():
    all_topic = get_all_topic()
    # return url_for('static', filename='css/style.css')
    return render_template('index.html',all_topic=all_topic)

@app.route('/admin')
@app.route('/admin/<languages>')
def admin(languages='?lang=zh_CN'):
    return '<a href="/admin/?lang=zh_CN">Click me to get to Admin!</a>'

@app.route("/algorithm")
def algorithm():
    all_topic = get_all_topic()
    # return redirect(url_for('show_summary'))
    return render_template('algorithm.html', all_topic=all_topic)

@app.route('/summary')
@app.route('/summary/<topic_name>')
def show_summary(topic_name='校园网大规模病毒攻击'):
    topic = '#'+topic_name+'#'
    all_topic = get_all_topic()
    summarys = Summary.query.filter_by(topic=topic ).all()
    weibos = Weibo.query.filter_by(topic=topic).all()
    keywords = Keywords.query.filter_by(topic=topic).all()
    results = Result.query.filter_by(topic=topic).all()
    result_array = get_result_array(results)
    return render_template('summary.html', summarys=summarys, weibos=weibos, keywords=keywords, results=result_array,all_topic=all_topic)

def get_result_array(results):
    method = []
    recall = []
    percise = []
    f_mesure = []
    sum_mesure = []
    for r in results:
        method.append(str(r.method))
        recall.append(r.recall)
        percise.append(r.percise)
        f_mesure.append(r.f_mesure)
        sum_mesure.append(r.sum_mesure)
    result_array = [method,recall,percise,f_mesure,sum_mesure]
    print result_array
    return result_array

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

def get_all_topic():
    return Topic.query.all()

def get_all_summary(topic):
    return Summary.query.filter_by(topic=topic).all()

# Model
class Weibo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120))
    content = db.Column(db.String(200))
    transfer = db.Column(db.String(50))
    like = db.Column(db.String(50))
    comment = db.Column(db.String(50))

    def __init__(self, topic=None, content=None, transfer=None, like=None, comment=None):
        self.topic = topic
        self.content = content
        self.transfer = transfer
        self.like = like
        self.comment = comment

    def __repr__(self):
        return '<Weibo> %r' % self.topic

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120))
    content = db.Column(db.String(200))
    content_segment = db.Column(db.String(200))
    method = db.Column(db.String(120))

    def __init__(self, topic=None, content=None, content_segment=None, method=None):
        self.topic = topic
        self.content = content
        self.content_segment = content_segment 
        self.method = method

    def __repr__(self):
        return '<Summary> %r' % self.topic

class Keywords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120))
    word = db.Column(db.String(120))
    weight = db.Column(db.Float)

    def __init__(self, topic=None, word=None, weight=None):
        self.topic = topic
        self.word = word
        self.weight = weight

    def __repr__(self):
        return '<Keywords.weight> %r' % self.weight

class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    intro = db.Column(db.String(200))
    comment = db.Column(db.String(120))

    def __init__(self, name=None, intro=None, comment=None):
        self.name = name
        self.intro = intro
        self.comment = comment

    def __repr__(self):
        return '<Method> %r' % self.name


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(120))
    topic = db.Column(db.String(120))
    percise = db.Column(db.Float)
    recall = db.Column(db.Float)
    f_mesure = db.Column(db.Float)
    sum_mesure = db.Column(db.Float)

    def __init__(self, method=None, topic=None, percise=None, recall=None, f_mesure=None, sum_mesure=None):
        self.method = method
        self.topic = topic
        self.percise = percise
        self.recall = recall
        self.f_mesure = f_mesure
        self.sum_mesure = sum_mesure

    def __repr__(self):
        return '<Result> %r' % self.method

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Method> %r' % self.name

# Admin View
class WeiboView(sqla.ModelView):
    column_filters = ('id', 'topic', 'transfer','like','comment')

class SummaryView(sqla.ModelView):
    column_filters = ('id', 'topic', 'content')

class KeywordsView(sqla.ModelView):
    column_filters = ('id', 'topic', 'word', 'weight')

class ResultView(sqla.ModelView):
    column_filters = ('id', 'topic', 'method')

class TopicView(sqla.ModelView):
    column_filters = ('id', 'name')

# Create admin
admin = Admin(app, '中文微博自动摘要-后台', template_mode='bootstrap3')

# Add views
admin.add_view(WeiboView(Weibo, db.session, name='微博'))
admin.add_view(SummaryView(Summary, db.session, name='摘要'))
admin.add_view(KeywordsView(Keywords, db.session, name='关键字'))
admin.add_view(ResultView(Result, db.session, name='评估结果'))
admin.add_view(TopicView(Topic, db.session, name='话题'))

path = op.join(op.dirname(__file__), '../weiboData')
try:
    os.mkdir(path)
except OSError:
    pass

raw_path = op.join(op.dirname(__file__), '../rawData')
try:
    os.mkdir(raw_path)
except OSError:
    pass

admin.add_view(FileAdmin(path, '../weiboData/', name='微博文件'))
admin.add_view(FileAdmin(raw_path, '../rawData/', name='原始文件'))



# Initialize babel
babel = Babel(app)

@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'en')

if __name__ == "__main__":
    app.run()
