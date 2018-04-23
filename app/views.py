"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""


from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, jsonify, make_response,session
from flask_login import login_user, logout_user, current_user, login_required
import requests
import urlparse
import random
from forms import *
from models import *
from imageGetter import *

###
# Routing for your application.
###


@app.route('/')
def index():
    form=UploadForm()
    """Render website's initial page and let VueJS take over."""
    return render_template('index.html', form=form)

@app.route('/api/users/register', methods=['POST'])
def upload():
    form=RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
       first_name = form.first_name.data
       last_name = form.last_name.data
       username = form.username.data
       password = form.password.data

       uid = genId(first_name,last_name,random.randint(1,100))

       new_user = UserProfile(userid=uid, username=username, first_name=first_name, last_name=last_name, password=password)

       db.session.add(new_user)
       db.session.commit()

       return "Success"
       
@app.route("/api/users/login", methods=["POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        uname = form.username.data
        pword = form.password.data

        user = UserProfile.query.filter_by(username=uname, password=pword).first()

        if user is not None:
            login_user(user)
            session["userid"] = user.userid
            flash('Logged in successfully.', 'success')
            #return redirect(url_for("secure_page")) # they should be redirected to a secure-page route instead

        else:
            flash('Username or Password is incorrect.', 'danger')
            #return
            

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages


###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

def genId(fname, lname, num):
    nid = []
    for x in fname:
        nid.append(str(ord(x)))
    for x in lname:
        nid.append(str(ord(x)))
    nid.append(str(num))

    random.shuffle(nid)

    nid = "".join(nid)

    return nid[:7]
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
