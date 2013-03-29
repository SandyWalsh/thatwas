import datetime

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from flask import flash
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for

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

    def __init__(self, tag, author, start, end, description):
        self.tag = tag
        self.author = author
        self.start = start
        self.end = end
        self.description = description

    def __repr__(self):
        return "<Event '%r'>" % self.tag


class EventForm(Form):
    tag = TextField('Tag', [validators.Length(min=1, max=15)])
    author = TextField('Email Address', [validators.Length(min=6, max=35)])
    start_datetime = DateTimeField('Start Date/Time', [validators.Required()],
                                            default=datetime.datetime.utcnow())
    end_datetime = DateTimeField('End Date/Time',
                                [validators.Required()],
                                default=datetime.datetime.utcnow() +
                                        datetime.timedelta(days=1))
    description = TextField('Description', [validators.Length(min=1, max=80)])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = EventForm(request.form)
    if request.method == 'POST' and form.validate():
        flash("The '%s' event has been recorded. Thanks!" % form.tag.data)
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run()
