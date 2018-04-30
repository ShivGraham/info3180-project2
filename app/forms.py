from flask_wtf import FlaskForm
from wtforms import FileField, PasswordField, SelectField, StringField, TextField, TextAreaField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import Email, InputRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class ProfileForm(FlaskForm):
    f_name = TextField('First Name', validators=[InputRequired()])
    l_name = TextField('Last Name', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')])
    email = TextField('Email', validators=[Email()])
    location = TextField('Location', validators=[InputRequired()])
    bio = TextAreaField('Biography', validators=[InputRequired()])
    photo = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[Email()])
    location = StringField('Location', validators=[InputRequired()])
    biography = TextAreaField('Biography',validators=[InputRequired()])
    profile_photo = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    
class NewPostForm(FlaskForm):
    photo = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    caption = TextAreaField('Biography',validators=[InputRequired()])
    
    