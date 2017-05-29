#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
# 2017-05-25

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:youxinyu@localhost:3306/weibodb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def get_all_summary(topic):
    return Summary.query.filter_by(topic=topic).all()
    # return Summary.query.filter_by(topic="#校园网大规模病毒攻击#").all()

class Actions():
    def show_all(self):
        allWeibo = Weibo.query.all()
        return allWeibo

class Weibo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120))
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

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return self.topic
        except Exception, e:
            print(e)
            db.session.rollback()
            return e
        finally:
            return 0
    
    def isExisted(self):
        temWeibo = Weibo.query.filter_by(topic=self.topic).first()
        if temWeibo is None:
            return 0
        else:
            return 1

    def echo(self):
        return 1


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120))
    content = db.Column(db.String(200))
    content_segment = db.Column(db.String(200))
    method = db.Column(db.String(120))

    def __init__(self, topic, content, content_segment, method):
        self.topic = topic
        self.content = content
        self.content_segment = content_segment 
        self.method = method

    def __repr__(self):
        return '<Summary> %r' % self.topic

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


class Keywords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(120))
    word = db.Column(db.String(120))
    weight = db.Column(db.Float)

    def __init__(self, topic, word, weight):
        self.topic = topic
        self.word = word
        self.weight = weight

    def __repr__(self):
        return '<Keywords.weight> %r' % self.weight

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


class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    intro = db.Column(db.String(200))
    comment = db.Column(db.String(120))

    def __init__(self, name, intro, comment):
        self.name = name
        self.intro = intro
        self.comment = comment

    def __repr__(self):
        return '<Method> %r' % self.name

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


class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(120))
    topic = db.Column(db.String(120))
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f_mesure = db.Column(db.Float)
    sum_mesure = db.Column(db.Float)

    def __init__(self, method, topic, precision, recall, f_mesure, sum_mesure):
        self.method = method
        self.topic = topic
        self.precision = precision
        self.recall = recall
        self.f_mesure = f_mesure
        self.sum_mesure = sum_mesure

    def __repr__(self):
        return '<Result> %r' % self.method
    
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

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Method> %r' % self.name

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