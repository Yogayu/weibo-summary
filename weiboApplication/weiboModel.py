#@author: youxinyu
#@data: 2017-05-25
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:youxinyu@localhost:3306/weibodb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Weibo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120), unique=True)
    content = db.Column(db.String(200))
    transfer = db.Column(db.String(50))
    like = db.Column(db.String(50))
    comment = db.Column(db.String(50))

    def __init__(self, topic, content, transfer, like, comment):
        self.topic = topic
        self.content = content
        self.transfer = transfer
        self.like = like
        self.comment = comment

    def __repr__(self):
        return '<Weibo> %r' % self.topic

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception, e:
            print(e)
            db.session.rollback()
            return e
        finally:
            return 0
    
    # def isExisted(self):
    #     temWeibo = Weibo.query.filter_by(topic=self.topic).first()
    #     if temWeibo is None:
    #         return 0
    #     else:
    #         return 1

    def echo(self):
        return 1


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120), unique=True)
    content = db.Column(db.String(200))
    method = db.Column(db.String(120), unique=True)

    def __init__(self, topic, content, method):
        self.topic = topic
        self.content = content
        self.method = method

    def __repr__(self):
        return '<Summary> %r' % self.topic


class Keywords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120), unique=True)
    word = db.Column(db.String(80))
    weight = db.Column(db.Integer)

    def __init__(self, topic, word, weight):
        self.topic = topic
        self.word
        self.weight

    def __repr__(self):
        return '<Summary> %r' % self.topic


class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    intro = db.Column(db.String(200))
    comment = db.Column(db.String(120))

    def __init__(self, name, intro, comment):
        self.name = name
        self.intro = intro
        self.comment = comment

    def __repr__(self):
        return '<Method> %r' % self.name


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(120), unique=True)
    topic = db.Column(db.String(120))
    percise = db.Column(db.Float)
    recall = db.Column(db.Float, unique=True)
    f_mesure = db.Column(db.Float)
    sum_mesure = db.Column(db.Float)

    def __init__(self, method, topic, percise, recall, f_mesure, sum_mesure):
        self.method = method
        self.topic = topic
        self.percise = percise
        self.recall = recall
        self.f_mesure = f_mesure
        self.sum_mesure = sum_mesure

    def __repr__(self):
        return '<Method> %r' % self.method