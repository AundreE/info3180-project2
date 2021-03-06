"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""


from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from forms import *
from models import *
import os, datetime
import jwt
from functools import wraps
import json

###
# Routing for your application.
###

'''
@app.route('/')
def index():
    form=UploadForm()
    return render_template('index.html', form=form)
'''
@app.route('/')
def home():
    """Render website's initial page and let VueJS take over."""
    return render_template('index.html')
    
def jwt_token(t):
    @wraps(t)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return jsonify({'error': 'Access Denied : No Token Found'}), 401
        else:
            try:
                userdata = jwt.decode(auth, app.config['SECRET_KEY'])
                currentUser = Users.query.filter_by(username = userdata['user']).first()
            except jwt.exceptions.InvalidSignatureError:
                return jsonify({'error':'Invalid Token'})
            except jwt.exceptions.DecodeError:
                return jsonify({'error': 'Invalid Token'})
            return t(currentUser,*args, **kwargs)
    return decorated
            
        
@app.route('/api/users/register',methods=["POST"])
def register():
    form = RegisterForm()
    
    if request.method=='POST' and form.validate_on_submit():
        
        try:
            uname = form.username.data
            pword = form.password.data
            location=form.location.data
            bio=form.biography.data
            lname=form.lastname.data
            fname=form.firstname.data
            mail=form.email.data
            photo = form.photo.data
            date = str(datetime.date.today())
            filename = secure_filename(photo.filename)
            
            user = Users(username=uname, password=pword, first_name=fname, last_name=lname, email=mail, location=location, biography=bio, profile_photo=filename, joined_on=date)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.session.add(user)
            db.session.commit()
            print "here"
            return jsonify(message = "User successfully registered")
            
            
        except Exception as e:
            db.session.rollback()
            print e
            return jsonify(errors=["Internal Error"])
    
    return jsonify(errors=flash_errors(form))
    

@app.route('/api/auth/login',methods=["POST"])
def login():
    form = LoginForm()
    
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = Users.query.filter_by(username=username).first()
        
        if user != None and check_password_hash(user.password, password):
            payload = {'user': user.username}
            jwt_token = jwt.encode(payload,app.config['SECRET_KEY'],algorithm = "HS256")
            response = {'message': 'User successfully logged in','token':jwt_token, "user_id": user.id}
            
            return jsonify(response)
            
        return jsonify(errors="Username or password is incorrect")
    
    return jsonify(errors=flash_errors(form))


@app.route('/api/auth/logout', methods = ['GET'])
def logout():
    return jsonify(message= "User successfully logged out.")
    
        
@app.route('/api/posts', methods = ['GET'])
def viewPosts():
    allPosts = Posts.query.all()
    posts = []
    
    
    for post in allPosts:
        user = Users.query.filter_by(id=post.user_id).first()
        postObj = {"id": post.id, "user_id": post.user_id, "username": user.username, "user_profile_photo": url_for('static', filename='uploads/'+user.profile_photo),"photo": post.photo, "caption": post.caption, "created_on": post.created_on, "likes": post.likes}
        posts.append(postObj)
        
    return jsonify(posts=posts)
    
    
    
@app.route('/api/users/<user_id>/posts', methods =['GET','POST'])
def posts(user_id):
    
    form = UploadForm()
    
    if request.method == 'GET':
        posts = Posts.query.filter_by(user_id = user_id).all()
        user_id = posts[0].user_id
        
        user = Users.query.filter_by(id=user_id).first()
        user_follower_count = len(Follows.query.filter_by(user_id=user.id).all())
        response = {"status": "ok", "post_data":{"firstname":user.first_name, "lastname": user.last_name, "location": user.location, "joined_on": user.joined_on, "bio": user.biography, "postCount": len(posts), "followers": user_follower_count, "profile_image": url_for('static', filename='uploads/'+user.profile_photo), "posts":[]}}
        
        for post in posts:
            postObj = {"id":post.id, "user_id": post.user_id, "photo": url_for('static', filename='uploads/'+post.photo), "caption": post.caption, "created_on": post.created_on, "likes": post.likes}
            response["post_data"]["posts"].append(postObj)
        
        return jsonify(response)
        
    if request.method == 'POST' and form.validate_on_submit:
        count = db.session.query(Posts).count()
        u_id = user_id
        photo = form.image.data
        filename = secure_filename(photo.filename)
        captn = form.caption.data
        create_date = str(datetime.date.today())
        post = Posts(user_id=u_id,photo=filename,caption=captn ,created_on=create_date)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        db.session.add(post)
        db.session.commit()
        return jsonify(post)
        

@app.route('/api/users/<user_id>/follow', methods = ['POST'])
def follow(user_id):
    if request.method == 'POST':
        u_id = user_id
        
        follow = Follows(user_id=u_id,follower_id=1)
        db.session.add(follow)
        db.session.commit()
    


# Like Route
@app.route('/api/posts/<post_id>/like',methods = ['POST'])
@jwt_token
def like(currentUser,post_id):
    post = Posts.query.filter_by(post_id).first()
    
    if not post:
        return flash_errors(['post does not exist'])
        
    if request.method == 'POST':
        like = Likes(post_id = request.values.get('post_id'),user_id = request.values.get('user_id'))
        db.session.add(like)
        db.session.commit()
        
        total_likes = len(Like.query.filter_by(postid = post_id).all())
        return jsonify({'message': 'post liked','likes':total_likes})
    return flash_errors(['Only POST requests are accepted'])
    
    

# Flash errors in case of failed validation
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")