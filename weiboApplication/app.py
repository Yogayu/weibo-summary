#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
import os
import os.path as op

from flask import Flask, url_for, request, redirect, make_response
from flask import render_template, json, session, flash
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.event import listens_for
from jinja2 import Markup

from flask_admin.form import rules
from flask_admin.contrib import sqla
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin import Admin, form, expose

from flask_babelex import Babel  # languages
from subprocess import call
from config import *
# login
from wtforms import form, fields, validators
import flask_admin as admin
import flask_login as login
from flask_admin import helpers, expose
from werkzeug.security import generate_password_hash, check_password_hash

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:youxinyu@localhost:3306/weibodb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# set flask admin swatch
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

basedir = get_base_dir()


@app.route("/")
def index():
    all_topic = get_all_topic()
    return render_template('index.html', all_topic=all_topic)

@app.route("/algorithm")
def algorithm():
    all_topic = get_all_topic()
    methods = Method.query.all()
    return render_template('algorithm.html', all_topic=all_topic, methods=methods)

@app.route('/summary')
@app.route('/summary/<topic_name>')
def show_summary(topic_name='新疆塔什库尔干5.5级地震'):
    if topic_name == '雄安新区' or topic_name == '豆瓣电影评分' or topic_name == '魏则西事件' or topic_name == '雾霾' or topic_name == '汽车':
        topic = topic_name
    else:
        topic = '#'+topic_name+'#'
    print topic
    all_topic = get_all_topic()
    summarys = Summary.query.filter_by(topic=topic).all()
    weibos = Weibo.query.filter_by(topic=topic).all()
    keywords = Keywords.query.filter_by(topic=topic).all()
    results = Result.query.filter_by(topic=topic).all()
    result_array = get_result_array(results)
    return render_template('summary.html', summarys=summarys, weibos=weibos, keywords=keywords, results=result_array, all_topic=all_topic)


def get_result_array(results):
    method = []
    recall = []
    precision = []
    f_mesure = []
    sum_mesure = []
    for r in results:
        method.append(str(r.method))
        recall.append(r.recall)
        precision.append(r.precision)
        f_mesure.append(r.f_mesure)
        sum_mesure.append(r.sum_mesure)
    result_array = [method, recall, precision, f_mesure, sum_mesure]
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


# Action

@app.route('/experiment', methods=['GET', 'POST'])
def experiment():
    if request.method == 'POST':
        topic = request.form.get('topic','default value')
        topic_type = request.form.get('type','topic')

        if topic == "":
            flash('话题不能为空')
            return redirect(url_for('admin.index'))
        else:
            return redirect(url_for('saveWeiboData',topic_name=topic,topic_type=topic_type))
    else:
        flash('Ops~, Not Post!')
        return redirect(url_for('admin.index'))

@app.route('/saveWeiboData')
@app.route('/saveWeiboData/<topic_name>/<topic_type>')
def saveWeiboData(topic_name=None,topic_type=None):
    if notUseableTopic(topic_name,topic_type) == 0:
        return redirect(url_for('admin.index'))
    topic_name = transTopic(topic_name,topic_type)
    
    Topic(topic_name.replace('\#',''), str(topic_type)).add()
    command = 'python processRawData.py' + ' ' + str(topic_name) + ' ' + str(topic_type)
    print command
    path = basedir + '/util/'
    print(call([command], shell=True, cwd=path))
    flash("预处理并存入数据库成功！")
    return redirect(url_for('admin.index'))

@app.route('/generateKeywords', methods=['GET', 'POST'])
def generateKeywords(topic_name=None,topic_type=None):
    if request.method == 'POST':
        topic_name = request.form.get('topic','default')
        topic_type = request.form.get('type','topic')

        if topic_name == "":
            flash('话题不能为空')
            return redirect(url_for('admin.index'))

        if notUseableWieboPath(topic_name,topic_type) == 0:
            return redirect(url_for('admin.index'))

        isExist = Keywords.query.filter_by(topic=topic_name).all()
        if isExist:
            flash("该话题已经生成过关键字，请在关键字表格中查看！")
            return redirect(url_for('admin.index'))

        topic_name = transTopic(topic_name,topic_type)

        command = 'python keywords.py' + ' ' + str(topic_name)
        print command
        path = basedir + '/util/'
        print(call([command], shell=True, cwd=path))
        flash("生成关键字成功！")
        return redirect(url_for('admin.index'))
    else:
        flash('Ops~, Not POST!')
        return redirect(url_for('admin.index'))

@app.route('/generateSummarys', methods=['GET', 'POST'])
def generateSummarys(topic_name=None,topic_type=None):
    if request.method == 'POST':
        topic_name = request.form.get('topic','default')
        topic_type = request.form.get('type','topic')

        if topic_name == "":
            flash('话题不能为空')
            return redirect(url_for('admin.index'))

        if notUseableWieboPath(topic_name,topic_type) == 0:
            return redirect(url_for('admin.index'))
        
        isExist = Summary.query.filter_by(topic=topic_name,method="Random").all()
        if isExist:
            flash("该话题已经生成过算法摘要，请在摘要表格中查看！")
            return redirect(url_for('admin.index'))
        
        topic_name = transTopic(topic_name,topic_type)

        command = 'python generateSummarys.py' + ' ' + str(topic_name)
        print command
        path = basedir + '/util/'
        print(call([command], shell=True, cwd=path))
        flash("生成算法摘要成功！")
        return redirect(url_for('admin.index'))
    else:
        flash('Ops~, Not POST!')
        return redirect(url_for('admin.index'))

@app.route('/generateManual', methods=['GET', 'POST'])
@app.route('/generateManual/<topic_name>/<topic_type>/<method>')
def addManaul(topic_name=None, topic_type=None, method=None):
    if request.method == 'POST':
            topic_name = request.form.get('topic','default')
            topic_type = request.form.get('type','topic')
            method = request.form.get('method','manual1')

            if topic_name == "":
                flash('话题不能为空')
                return redirect(url_for('admin.index'))

            if notUsableManualPath(topic_name,topic_type,method) == 0:
                return redirect(url_for('admin.index'))
            print method
            isExist = Summary.query.filter_by(method=method,topic=topic_name).all()
            print isExist
            if isExist:
                alert_string = "该话题已经生成过"+method+"的人工摘要，请在摘要表格中查看！"
                flash(alert_string)
                return redirect(url_for('admin.index'))
            
            topic_name = transTopic(topic_name,topic_type)

            command = 'python manualSegment.py' + ' ' + str(topic_name) + ' ' + str(method)
            print command
            path = basedir + '/util/'
            print(call([command], shell=True, cwd=path))
            flash("人工摘要添加成功！")
            return redirect(url_for('admin.index'))
    else:
        flash('Ops~, Not POST!')
        return redirect(url_for('admin.index'))


@app.route('/deleteAllRouge')
def deleteAllRouge():
    # 先清空数据
    try:
        num_rows_deleted = db.session.query(Result).delete()
        db.session.commit()
    except:
        db.session.rollback()
    print 'delete'
    # db.session.query(Result).delete(synchronize_session=False)
    flash('所有摘要的ROUGE评估删除成功！')
    return redirect(url_for('admin.index'))

@app.route('/calculateAllRouge')
def calculateAllRouge():
    # 先清空数据
    try:
        num_rows_deleted = db.session.query(Result).delete()
        db.session.commit()
    except:
        db.session.rollback()
    
    print 'delete'

    command = 'python calculateAllRouge.py'
    path = basedir + '/util/'
    print(call([command], shell=True, cwd=path))
    flash('生成所有摘要的ROUGE评估结果成功！请到表格中查看')
    return redirect(url_for('admin.index'))

def notUseableTopic(topic_name, topic_type):
    print topic_name
    isExist = Topic.query.filter_by(name=topic_name.replace('#','')).all()
    print 'isExist'
    print isExist
    if isExist:
        flash('话题已经存在，请另外输入')
        return 0
    path = get_base_dir() + '/Data/rawData/' + topic_type + '/' + topic_name 
    print path
    if os.path.exists(path):
        return 1
    else:
        flash('原始数据文件夹不存在,请先上传文件夹到/Data/RawData/Topice(Keyword)路径, 命名方式为“话题名”')
        print("话题路径不存在")
        return 0

def notUseableWieboPath(topic_name, topic_type):
    path = get_base_dir() + '/Data/weiboData/' + topic_name + '.txt'
    print path
    if os.path.exists(path):
        return 1
    else:
        flash('微博文件路径不存在,请先生成微博文件')
        print("微博路径不存在")
        return 0

def notUsableManualPath(topic_name, topic_type, method):
    # topic_name = 
    path = get_base_dir() + '/Data/ROUGE/manual_sentences/' + topic_name + '-' + method + '.txt'
    print path
    if os.path.exists(path):
        return 1
    else:
        flash('人工摘要不存在,请先上传文件到/Data/ROUGE/manual_sentences, 命名方式为“话题名-manual1/2/3.txt”')
        print("人工摘要不存在")
        return 0

def transTopic(topic_name, topic_type):
    # if topic_type == 'Topic':
    topic_name = str(topic_name).replace('#','\#')
    return topic_name

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

    def isExist(self):
        result = Weibo.query.filter_by(topic=self.topic).all()
        if result:
            return 1
        else:
            return 0

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

    def isExist(self):
        result = Summary.query.filter_by(topic=self.topic).all()
        if result:
            return 1
        else:
            return 0


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
    def isExist(self):
        result = Keywords.query.filter_by(topic=self.topic).all()
        if result:
            return 1
        else:
            return 0

class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    intro = db.Column(db.String(800))
    comment = db.Column(db.String(120))

    def __init__(self, name=None, intro=None, comment=None):
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

    def isExist(self):
        result = Method.query.filter_by(topic=self.topic).all()
        if result:
            return 1
        else:
            return 0

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(120))
    topic = db.Column(db.String(120))
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f_mesure = db.Column(db.Float)
    sum_mesure = db.Column(db.Float)
    manual_evaluation = db.Column(db.Float)

    def __init__(self, method=None, topic=None, precision=None, recall=None, f_mesure=None, sum_mesure=None, manual_evaluation=None):
        self.method = method
        self.topic = topic
        self.precision = precision
        self.recall = recall
        self.f_mesure = f_mesure
        self.sum_mesure = sum_mesure
        self.manual_evaluation = manual_evaluation

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

    def isExist(self):
        result = Result.query.filter_by(topic=self.topic).all()
        if result:
            return 1
        else:
            return 0

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    type = db.Column(db.String(120))

    def __init__(self, name=None, topic_type=None):
        self.name = name
        self.type = topic_type

    def __repr__(self):
        return '<Topic> %r' % self.name

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

    def isExist(self):
        result = Topic.query.filter_by(topic=self.topic).all()
        if result:
            return 1
        else:
            return 0

# Create user model.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(64))

    def __init__(self, login=None, password=None):
        self.login = login
        # self.password = generate_password_hash(password)
        self.password = password

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

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username


#login forms
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()

class RegistrationForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    # email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError('Duplicate username')


# Initialize flask-login
def init_login():
    # test_user = User(login="test", password=generate_password_hash("test"))
    # db.session.add(test_user)
    # db.session.commit()

    login_manager = login.LoginManager()
    login_manager.init_app(app)

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)

# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated

# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        topics = get_all_topic()
        self._template_args['topics'] = topics
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))
        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link

        return super(MyAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        form = RegistrationForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = User()

            form.populate_obj(user)
            # we hash the users password to avoid saving it as plaintext in the db,
            # remove to use plain text:
            user.password = generate_password_hash(form.password.data)
            user.id = 10
            # db.session.add(user)
            user.add()
            # db.session.commit()

            login.login_user(user)
            return redirect(url_for('.index'))
        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
        self._template_args['form'] = form
        self._template_args['link'] = link
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))

# Admin View


class WeiboView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    column_filters = ('id', 'topic', 'transfer', 'like', 'comment')


class SummaryView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    column_filters = ('id', 'topic', 'content', 'method')


class KeywordsView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    column_filters = ('id', 'topic', 'word', 'weight')


class ResultView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    column_filters = ('id', 'topic', 'method', 'precision',
                      'recall', 'f_mesure', 'sum_mesure', 'manual_evaluation')


class TopicView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    column_filters = ('id', 'name', 'type')

class MethodView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated
    column_filters = ('name', 'intro', 'comment')
     
class MyFileAdmin(FileAdmin):
    def is_accessible(self):
        return login.current_user.is_authenticated

    def get_base_path(self):
        path = FileAdmin.get_base_path(self)
        return path


# Initialize flask-login
init_login()

# Create admin
# admin = Admin(app, '中文微博自动摘要-后台', template_mode='bootstrap3')
admin = Admin(app, '中文微博自动摘要-后台', index_view=MyAdminIndexView(), template_mode='bootstrap3')
# Add views
# admin.add_view(MyModelView(User, db.session, name='管理员'))
admin.add_view(TopicView(Topic, db.session, name='话题'))
admin.add_view(WeiboView(Weibo, db.session, name='微博'))
admin.add_view(SummaryView(Summary, db.session, name='摘要'))
admin.add_view(KeywordsView(Keywords, db.session, name='关键字'))
admin.add_view(ResultView(Result, db.session, name='评估结果'))
admin.add_view(MethodView(Method, db.session, name='算法'))

path = op.join(op.dirname(__file__), 'Data')
try:
    os.mkdir(path)
except OSError:
    pass
admin.add_view(MyFileAdmin(path, 'Data/', name='文件管理'))

# language
babel = Babel(app)

@babel.localeselector
def get_locale():
    override = request.args.get('lang')
    if override:
        session['lang'] = override
    return session.get('lang', 'zh_CN')

if __name__ == "__main__":
    app.run()
