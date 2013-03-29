import datetime

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask import flash
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for

from sqlalchemy import desc
from sqlalchemy.exc import OperationalError

from wtforms import Form, TextField, validators
from wtforms.ext.dateutil.fields import  DateTimeField


app = Flask(__name__)
app.debug = True
app.secret_key = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/thatwas.db'
db = SQLAlchemy(app)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(15), index=True)
    author = db.Column(db.String(35))
    start = db.Column(db.DateTime(), index=True)
    end = db.Column(db.DateTime(), index=True)
    description = db.Column(db.String(80))
    processed = db.Column(db.Boolean(), index=True)


    def __init__(self, tag, author, start, end, description):
        self.tag = tag
        self.author = author
        self.start = start
        self.end = end
        self.description = description
        self.processed = False

    def __repr__(self):
        return "<Event '%r'>" % self.tag


class EventForm(Form):
    now = datetime.datetime.utcnow()
    now = now.replace(second=0, microsecond=0)
    tag = TextField('Tag', [validators.Length(min=1, max=15)])
    author = TextField('Email Address', [validators.Length(min=6, max=35)])
    start_datetime = DateTimeField('Start Date/Time', [validators.Required()],
                                            default=now)
    end_datetime = DateTimeField('End Date/Time',
                                [validators.Required()],
                                default=now)
    description = TextField('Description', [validators.Length(min=1, max=80)])


@app.route('/', methods=['GET', 'POST'])
def index():
    events = Event.query.order_by(desc(Event.start))

    form = EventForm(request.form)
    if request.method == 'POST' and form.validate():
        flash("The '%s' event has been recorded. Thanks!" % form.tag.data)
        event = Event(form.tag.data,
                      form.author.data,
                      form.start_datetime.data,
                      form.end_datetime.data,
                      form.description.data)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form, events=events)


@app.route('/add', methods=['POST'])
def add():
    start = datetime.datetime.strptime(request.form['start'],
                                       "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(request.form['end'],
                                       "%Y-%m-%d %H:%M:%S")
    event = Event(request.form['tag'],
                  request.form['author'],
                  start, end,
                  request.form['description'])
    db.session.add(event)
    db.session.commit()
    return "Ok"


@app.route('/rm', methods=['POST'])
def rm():
    eid = int(request.form['eid'])
    event = Event.query.filter_by(id=eid).first_or_404()
    db.session.delete(event)
    db.session.commit()
    return "Ok"



if __name__ == "__main__":
    try:
        for x in Event.query.limit(1):
            pass
        print "Using existing db."
    except OperationalError:
        print "Creating db"
        db.create_all()

    app.run()
