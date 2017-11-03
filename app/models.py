from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    #ENsure table will be name in plural an not in singular
    # as is the name ot the Model
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key =True)
    email = db.Column(db.String(60), index = True, unique = True)
    username = db.Column(db.String(60), index = True, unique = True)
    first_name = db.Column(db.String(60), index = True)
    last_name = db.Column(db.String(60), index = True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default =False)


    @property
    def password(self):
        """
        Prevent password from being accessed
        """

        raise AttributeError('password is not a reabale attribute')


    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        """
        Check if hashed password matches actual password
        """

        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<User: {}>'.format(self.username)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Player( db.Model):
    """
    Create an Player table
    """

    #ENsure table will be name in plural an not in singular
    # as is the name ot the Model
    __tablename__ = 'players'


    id = db.Column(db.Integer, primary_key =True)
    email = db.Column(db.String(60), index = True, unique = True)
    username = db.Column(db.String(60), index = True, unique = True)
    first_name = db.Column(db.String(60), index = True)
    last_name = db.Column(db.String(60), index = True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    def __repr__(self):
        return '<Player: {}>'.format(self.username)



class Team(db.Model):
    """
    Create a teams table
    """

    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), unique = True)
    history = db.Column(db.String(200))
    players = db.relationship('Player', backref ='team', lazy ='dynamic')


    def __repr__(self):
        return '<Team: {}>'.format(self.name)
