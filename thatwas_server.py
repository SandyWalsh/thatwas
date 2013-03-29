import datetime

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


class EventForm(Form):
    tag = TextField('Tag', [validators.Length(min=1, max=15)])
    author = TextField('Email Address', [validators.Length(min=6, max=35)])
    start_datetime = DateTimeField('Start', [validators.Required()],
                                            default=datetime.datetime.utcnow())
    end_datetime = DateTimeField('End',
                                [validators.Required()],
                                default=datetime.datetime.utcnow() +
                                        datetime.timedelta(days=1))
    description = TextField('Description', [validators.Length(min=1, max=80)])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = EventForm(request.form)
    if request.method == 'POST' and form.validate():
        flash("The '%s' event has been recorded. Thanks!" % form.tag.data)
        print "FLASH"
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run()
