#  引入flask_wtf
from flask_wtf import FlaskForm
#  各別引入需求欄位類別
from wtforms import StringField, SubmitField, SelectField, validators
from wtforms.fields.html5 import EmailField
#  引入驗證
#from wtforms.validators import DataRequired, Email

#  從繼承FlaskForm開始
class UserForm(FlaskForm):
  username = StringField('UserName', validators=[validators.Required(message='Not Null')])
  email = EmailField('Email', validators=[validators.Required(message='Not Null')])
  language = SelectField('語言', choices = [('cpp', 'C++'), ('py', 'Python')])
  submit = SubmitField('Submit')

