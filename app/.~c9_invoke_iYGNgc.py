"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash,make_response,abort
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm, ProfileForm, RegisterForm, NewPostForm
from models import Users,Follows,Likes, Posts
from werkzeug.security import check_password_hash,generate_password_hash
from werkzeug.utils import secure_filename
from flask import jsonify, g, session
from sqlalchemy.sql import text
import json
import datetime
import random

# Using JWT
import jwt
from flask import _request_ctx_stack
from functools import wraps
import base64
import os

# MIGHT NEED TO BE TWEAKED
# Create a JWT @requires_auth decorator
# This decorator can be used to denote that a specific route should check
# for a valid JWT token before displaying the contents of that route.
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None)
    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
         payload = jwt.decode(token,app.config['SECRET_KEY'])

    except jwt.ExpiredSignature:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated

###
# Routing for your application.
###

###
# API Routes
###
@app.route('/api/users/register', methods=["POST"])
def register():
    """ Allows for a new user to register for Photogram """
    
    rForm = RegisterForm()
    uFolder = app.config['UPLOAD_FOLDER']
    
    
    if request.method == "POST" and rForm.validate_on_submit():
        u_name = request.form['username']
        pwd = request.form['password']
        pwd = generate_password_hash(pwd)
        f_name = request.form['firstname']
        l_name = request.form['lastname']
        email = request.form['email']
        location = request.form['location']
        bio = request.form['biography']
        
        image_file = request.files['profile_photo']
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(uFolder, filename))
        
        now = datetime.datetime.now()
        joined = "" + format_date_joined(now.year, now.month, now.day)
        
        user = Users(u_name, pwd, f_name, l_name, email, location, bio, filename, joined)
        
        db.session.add(user)
        db.session.commit()
       
        
        info = {'message': 'User successfully registered'}
        
        return jsonify(info=info)
    else:
        errors = form_errors(rForm)
        
        return jsonify(errors=errors),2

@app.route('/api/auth/login', methods=["POST"])
def login():
    """ Accepts login credentials for a user """
    
    lForm = LoginForm()
    
    if request.method == "POST" and lForm.validate_on_submit():
        uname = request.form['username']
        pwd = request.form['password']
        
        user = Users.query.filter_by(username=uname).first()
        #user = db.session.query(User).filter_by(username=uname).first()
       
        if user is not None and check_password_hash(user.password, pwd):
        #if user is not None:
            payload = {'user_id': user.id, 'uname': uname}
            token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
            
            info = {'token': token, 'message': 'User successfully logged in.'}
            
            return jsonify(info=info)
        else:
            errors = {'errors': 'Incorrect username and/or password'}
            
            return jsonify(errors=errors)
    else:
        errors = form_errors(lForm)
        
        return jsonify(errors=errors)
           

@app.route('/api/auth/logout', methods=['GET'])
@requires_auth
def logout():
    """ Logout a user """
    
    info = {'message': 'User successfully logged out.'}
    
    return jsonify(info=info)
 
@app.route('/api/posts', methods=['GET'])
@requires_auth
def all_posts():
    """ Returns all users' posts """
    
    posts_list = []
    
    posts = Posts.query.order_by(Posts.created_on.desc()).all()
    
    for post in posts:
        uname = Users.query.get(post.user_id).username
        likes = getLikes(post.id)
        
        posts_list += [{'id': post.id, 'user_id': post.user_id, 'username': uname, 'photo': post.photo, 'caption': post.caption, 'created_on': post.created_on, 'likes': likes}]
    
    info = {'posts': posts_list}
    
    #posts_list = [{'id': 1, 'user_id': 1, 'username': 'The Weeknd', 'photo': "weeknd.jpg", 'caption': "Weeknd Vibes", 'created_on': "2018-04-05 14:25:00", 'likes': 10}]
    #posts_list += [{'id': 2, 'user_id': 2, 'username': 'Sana', 'photo': "sana.jpg", 'caption': "Sana", 'created_on': "2018-04-06 13:15:00", 'likes': 100}]
    
    #info = {'posts': posts_list}
    
    return jsonify(info=info)

def getLikes(post_id):
    
    #query = text("SELECT COUNT(DISTINCT Likes.id) FROM Likes JOIN Posts ON WHERE Posts.id = Follows.follower_id  ")
    #likes_count = db.session.execute(query)
    
    count = 0
    
    likes = Likes.query.filter_by(post_id=post_id).all()
    
    for like in likes:
        count += 1
    
    return count
    
@app.route('/api/users/<user_id>/posts', methods=['GET'])
@requires_auth
def posts(user_id):
    posts_list = []
    
    posts = Posts.query.filter_by(user_id=user_id).all()
    
    for post in posts:
        posts_list += [{'id': post.id, 'user_id': post.user_id, 'photo': post.photo, 'description': post.caption, 'created_on': post.created_on}]
    
    info = {'posts': posts_list}
    
    #try this
    #output = []

    # for post in posts:
	   # post_list = {}
    # 	post_list['id'] = post.id
	   # post_list['user_id'] = post.user_id
	   # post_list['photo'] = post.photo
	   # post_list['description'] = post.description
	   # post_list['created_on'] = post.created_on
	   # output.append(post_list)
    #info = { 'posts' : output }
    return jsonify(info=info)

@app.route('/api/users/<user_id>/posts', methods=['POST'])
@requires_auth
def add_posts(user_id):
    pForm = NewPostForm()
    uFolder = app.config['UPLOAD_FOLDER']
    
    myid = int(user_id)
    
    if request.method == "POST" and pForm.validate_on_submit():
        caption = request.form['caption']
        pic = request.files['photo']
        
        filename = secure_filename(pic.filename)
        pic.save(os.path.join(uFolder, filename))
        
        now = datetime.datetime.now()
        created = "" + format_date_joined(now.year, now.month, now.day)
        
        myPost = Posts(myid, filename, caption, created)
        
        db.session.add(myPost)
        db.session.commit()
        
        info = {'message': 'Successfully created a new post'}
        
        return jsonify(info=info)
    else:
        errors = form_errors(pForm)
        
        return jsonify(errors=errors)


@app.route('/api/users/<user_id>/follow', methods=['POST'])
@requires_auth
def follow(user_id):
    if request.method == "POST":
        ### Follow a user ###
        current_id = g.current_user['user_id'] # get follower
        
        relation = Follows.query.filter_by(user_id=current_id, follower_id=user_id).first()
        
        if relation is None:
            follow = Follows(user_id, current_id)
            db.session.add(follow)
            db.session.commit()
            
            info = {'message': 'You are now following that user.'}
        else:
            info = {'error': 'You are already following this user!'}
            
        return jsonify(info=info)
    
#Get the number of followers
@app.route('/api/users/<user_id>/follow', methods=['GET'])
@requires_auth
def get_followers(user_id):
    query = text("""SELECT COUNT(DISTINCT f.follower_id) as followers FROM Follows f WHERE f.user_id = :id""")
    follower_count = db.session.get_bind().execute(query, id=user_id)
    if follower_count:
        for f in follower_count:
            info = {'followers': f.followers }
            return jsonify(info=info)
    else:
        err = {'error': 'An error occurred.'}
        return jsonify(error=err)    
        
# @app.route('/api/users/<user_id>/follow', methods=['GET'])
# @requires_auth
# def followers(user_id):
    
#     followers = Follows.query.filter_by(user_id=user_id).all()
    
#     count = 0
    
#     for follower in followers:
#         count += 1
        
#     info = {'followers': count}
    
#     return jsonify(info=info)
    
@app.route('/api/posts/<post_id>/like', methods=['POST'])
@requires_auth
def likes(post_id):
    
    #Get the current user
    current_user_id = g.current_user['user_id']
    
    like_exists = Likes.query.filter_by(user_id=current_user_id, post_id=post_id).first()
    
    if like_exists is None:
        #Insert query
        likes = Likes(current_user_id,post_id)
        db.session.add(likes)
        db.session.commit()
        #Get updated number of likes on the post
        num_likes = getLikes(post_id)
        info = {'message': 'Post liked!', 'likes': num_likes}
    else:
        info = {'error': 'You have already liked this post!'}
        
    return jsonify(info=info)

@app.route('/api/users/<user_id>', methods=['GET'])
@requires_auth
def get_profile(user_id):
    ''' View a user's profile info'''
    users = Users.query.filter_by(id=user_id).first()
    if users is None:
        info = {'error': 'This user does not exist'}
    else:
        # get user info
        user = {'id': users.id, 'username': users.username, 'first_name': users.first_name, 'last_name': users.last_name, 'email': users.email, 'location': users.location, 'bio': users.bio, 'profile_photo': users.profile_photo, 'joined_on': users.joined_on}
        # Fetch user's posts
        posts = Posts.query.filter_by(user_id=user_id).all()
        if posts is None:
            info = {'user': user, 'posts': []}
        else:
            posts_list = [{'id': post.id, 'user_id': post.user_id, 'photo': post.photo, 'description': post.caption, 'created_on': post.created_on} for post in posts]
            info = {'user': user, 'posts': posts_list}
    return jsonify(info=info)
# Registers new users
#@app.route('/api/users/register', methods=['POST'])
#def register():
    #NOTES FROM JAV
    #Use WTF
    #We don't need a loop -> database auto generates the id
    #return a success message
    #uFolder = app.config['UPLOAD_FOLDER']
    
    #Retrieve the JSON object
    #data = request.get_json()
    #Retrieve the different key pairings in the JSON Object
    #fname = data['firstname']
    #lname = data['lastname']
    #uname = data['username']
    #pwd =  generate_password_hash(data['password'],method = 'sha256')
    #email = data['email']
    #location = data['location']
    #bio = data['biography']
    #photo = data['profile_photo']
        
    #img_name = secure_filename(photo.filename)
    #photo.save(os.path.join(uFolder,img_name))
        
        # Loop to find a unique id
    #while True:
        # Generate a random userid
        #userid = random.randint(620000000, 620099999)
        # Search for this userid
        #result = User.query.filter_by(id=userid).first() 
        # Check if not found
        #if result is None:
            # Unique; Exit loop
            #break
        
    #now = datetime.datetime.now()
    #joined = "" + format_date_joined(now.year, now.month, now.day)
   
    #Create the new User
    #Id to be generated
    #user = User(userid,fname,lname,email,location,bio,img_name,joined, uname, pwd)
      
    #Add the user  
    #db.session.add(user)
       
    #Save user to database
    #db.session.commit()
    #return make_response('User successfully registered',201,{"message": "User successfully registered"})
    
    ############################################################################
    
    # uFolder = app.config['UPLOAD_FOLDER']
    # form = RegisterForm()
    
    # if request.method == "POST":
    #     if form.validate_on_submit:
    #         username = form.username.data
    #         password = form.username.data
    #         firstname = form.firstname.data
    #         lastname = form.lastname.data
    #         email = form.email.data
    #         location = form.location.data
    #         biography = form.biography.data
    #         img = form.photo.data
    #         img_name = secure_filename(img.filename)
    #         img.save(os.path.join(uFolder,img_name))
            
    #         now = datetime.datetime.now()
    #         joined = "" + format_date_joined(now.year, now.month, now.day)
            
    #         user = User(firstname, lastname, email, location, biography, img_name, joined)
            
    #         db.session.add(user)
    #         db.session.commit()
    #         #return jsonify({'message' : 'User successfully registered'})
    #         return make_response('User successfully registered',201,{  "message": "User successfully registered"}) 
    # return jsonify(errors=form_errors(form))
    
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


#Login
#@app.route('/api/auth/login', methods=['POST'])
#def login():
    
    #Get authorization info
    #auth = request.authorization
    
    #Retrieve the JSON data
    #uname = auth['username']
    #pwd = auth['password']
    
    #Check if authorization info is completed
    #if not auth or not auth.username or not auth.password:
        #abort(400)
    
    #Check if the user exists in the db    
    #user = User.query.filter_by(username = auth.username).first()

    #if not user:
        #return jsonify({'message' : 'No user found.'})
     
    #Check if password matches   
    #if check_password_hash(user.password,auth.password): 
        #Generate the token
        #token = jwt.encode({'username' : user.username}, app.config['SECRET_KEY'], algorithm='HS256')
        #return jsonify({'token' : token, 'message': 'User successfully logged in.'}),200
        
    ############################################################################
    
    # form = LoginForm()
    # if request.method == "POST":
    #     if form.validate_on_submit():
            
    #         username = form.username.data
    #         password = form.password.data
            
    #         user = User.query.filter_by(username=username, password=password).first()
            
    #         if user is None:
    #             flash("Sorry, there is no such user.","warning")
    #         else:
    #             login_user(user) #I'm not sure if we're supposed to be using this
    #             payload = {'u_name': user.username}
    #             token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    #             # return jsonify(error=None, data={'token': token}, message="Token Generated")
        query = text("""SELECT COUNT(DISTINCT follower_id) as f FROM Follows WHERE Follows.user_id = :id""")
    # return jsonify("login.html", form=form) #This seems wrong
    
@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
@app.route('/')
def home():
    return render_template('home.html')
'''

@app.route('/profile', methods=["GET", "POST"])
def addProfile():
    pForm = ProfileForm()
    uFolder = app.config['UPLOAD_FOLDER']
    
    if request.method == "POST" and pForm.validate_on_submit():
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        gender = request.form['gender']
        email = request.form['email']
        location = request.form['location']
        bio = request.form['bio']
        
        image_file = request.files['photo']
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(uFolder, filename))
        
        now = datetime.datetime.now()
        joined = "" + format_date_joined(now.year, now.month, now.day)
        
        user = UserProfile(f_name, l_name, gender, email, location, bio, filename, joined)
        
        db.session.add(user)
        db.session.commit()
        
        flash('New profile added!', 'sucess')
        return redirect(url_for('listProfiles'))
    return render_template('profile.html', pForm=pForm) 
    

@app.route('/profiles')
def listProfiles():
    users = db.session.query(UserProfile).all()
    return render_template('profiles.html', users=users)
   
@app.route('/profile/<userid>', methods=["GET", "POST"])
def showProfile(userid):
    userid = str(userid)
    
    user = UserProfile.query.filter_by(id=userid).first()
    
    return render_template('user_profile.html', user=user)
    
    
'''
    
###
#  Helper Functions
###

#This function stores the names of the uploaded images in the uploads folder and returns them as a list

def get_uploaded_images():
    rootdir = os.getcwd()
    
    file_list = []
    
    for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
        for file in files:
		    name, ext = os.path.splitext(file)
		    if ((ext == '.jpg') or (ext == '.jpeg') or (ext == '.png')):
		        file_list.append(file)
	return file_list
	
#This function returns the date in the format yyyy/mm/dd	

def format_date_joined(year, month, day):
    date_joined = datetime.date(year, month, day)
    return date_joined.strftime("%B %d, %Y")	
    
#@app.route("/login", methods=["GET", "POST"])
#def login():
#    form = LoginForm()
#    if request.method == "POST":
        # changed this to actually validate the entire form submission
        # and not just one field
#        if form.validate_on_submit():
#            u_name = form.username.data
#            pwd = form.password.data
            
#            user = UserProfile.query.filter_by(username=u_name, password=pwd).first()
            
#            if user is not None and check_password_hash(user.pwd, pwd):
#                remember_me = False

#                if 'remember_me' in request.form:
#                    remember_me = True
#                # get user id, load into session
#                login_user(user, remember=remember_me)

                # remember to flash a message to the user
#                flash('Successfully logged in', 'success')
#                return redirect(url_for('secure_page'))  # redirected to a secure-page route instead
#            else:
#                flash('Username or Password is incorrect.', 'danger')

#    flash_errors(form)
#    return render_template("login.html", form=form)

#@app.route('/logout')
#@login_required
#def logout():
#    """Logs out current user"""
#    logout_user()
    
#    flash ('You are now logged out', 'danger')
#    return redirect( url_for('home'))


@app.route('/secure-page')
@login_required
def secure_page():
    """Renders a secure page that only logged in users can access."""
    return render_template('secure_page.html')

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
#@login_manager.user_loader
#def load_user(id):
#    return UserProfile.query.get(int(id))

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
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
