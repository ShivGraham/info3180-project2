from . import db

    
class Users(db.Model):
   # __tablename__ = 'user_profiles'
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    location = db.Column(db.String(50))
    bio = db.Column(db.String(100))
    profile_photo = db.Column(db.String(100))
    joined_on = db.Column(db.String(14))
    #addresses = relationship("Address", backref="user")
    
    #commented for testing
    link = db.relationship('Posts', backref='Users', lazy=True)
    link1 = db.relationship('Likes', backref ='Users', lazy=True)
    link2 = db.relationship('Follows', backref ='Users', lazy=True)
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __init__(self, username, password, first_name, last_name, email, location, bio, profile_photo, joined_on):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.location = location
        self.bio = bio
        self.profile_photo = profile_photo
        self.joined_on = joined_on
        
    def __repr__(self):
        return '<User %r>' % (self.first_name)

class Posts(db.Model):
    
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photo = db.Column(db.String(100))
    caption = db.Column(db.String(255))
    created_on = db.Column(db.String(14))
    link1 = db.relationship('Likes', backref='posts', lazy=True)
    
    # def is_active(self):
    #     return True
    
    # def get_id(self):
    #     try:
    #         return unicode(self.id)  # python 2 support
    #     except NameError:
    #         return str(self.id)  # python 3 support
            
    def __init__(self,user_id, photo, caption, created_on):
        self.photo = photo
        self.user_id = user_id
        self.caption = caption
        self.created_on = created_on
        
class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    
    # def is_active(self):
    #     return True
    
    # def get_id(self):
    #     try:
    #         return unicode(self.id)  # python 2 support
    #     except NameError:
    #         return str(self.id)  # python 3 support
            
    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id
    
class Follows(db.Model):
    #__tablename__ = 'follows'
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    follower_id = db.Column(db.Integer)
    
    # def is_active(self):
    #     return True
    
    # def get_id(self):
    #     try:
    #         return unicode(self.id)  # python 2 support
    #     except NameError:
    #         return str(self.id)  # python 3 support
            
    def __init__(self,user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id