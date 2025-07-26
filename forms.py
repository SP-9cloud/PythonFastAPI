from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,TextAreaField,SubmitField,RadioField,SelectField
from wtforms import validators,ValidationError

class ContactForm(FlaskForm):
    name = StringField("Name of Student", [validators.DataRequired("Please enter your name.")])
    gender=RadioField("Gender",choices=[('M','Male'),('F','Female')])
    address=TextAreaField("Address")
    email=StringField("Email",[validators.DataRequired("Please enter your email address."),validators.Email("Please enter valid email.")])
    age=IntegerField("age")
    language=SelectField("Languages",choices=[('cpp','c++'),('py','Python')])
    submit=SubmitField("Send")