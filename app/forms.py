from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.fields import TextAreaField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators = [DataRequired(), Email()])
    location = StringField("Location", validators = [DataRequired()])
    biography = TextAreaField("Biography", validators = [DataRequired()])
    photo = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class UploadForm(FlaskForm):
    image = FileField('Profile Picture', validators=[FileRequired(), FileAllowed(['jpg','png'],'Image only!')])
    caption = TextAreaField('Caption', validators=[DataRequired()]) 