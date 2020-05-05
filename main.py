from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired

class ContactForm(FlaskForm):

  name = StringField("Fullname", validators=[InputRequired('Please enter your name.')])

  email = StringField("Email",  validators=[InputRequired("Please enter your email address.")])

  password = StringField("Password",  validators=[InputRequired("Please enter your email password.")])

  recipient = StringField("Recipient", validators=[InputRequired("Please enter recipient's email.")])

  subject = StringField("Subject", validators=[InputRequired("Please enter your subject of email.")])

  text = TextAreaField("Email text", validators=[InputRequired("Please enter your text of email.")])

  submit = SubmitField("Send")

from flask import Flask, render_template, request, flash
from flask_mail import Message, Mail
import os
app = Flask(__name__)
app.secret_key = 'development key'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True

@app.route('/')
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('login.html', form=form)
        else:
            app.config["MAIL_USERNAME"] = form.email.data
            app.config["MAIL_PASSWORD"] = form.password.data
            msg = Message(form.subject.data, sender=str(form.name.data), recipients=[form.recipient.data])
            msg.html = render_template('Template.html', name=form.name.data, subject=form.subject.data, text=form.text.data)
            mail = Mail(app)
            mail.send(msg)
            return render_template('login.html', success=True)

    elif request.method == 'GET':
        return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
