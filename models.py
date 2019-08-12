from reading import db,login_manager,app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(255))
    password = db.Column('password',db.String(255))
    email = db.Column('email',db.String(255))

    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

class Books(db.Model):
    __tablename__ = 'books'
    bookid = db.Column('bookid',db.Integer,primary_key=True)
    bookname = db.Column('bookname',db.String(255))
    booktype = db.Column('booktype',db.String(255))
    author = db.Column('author',db.String(255))
    image = db.Column('image',db.String(255))
    introduction = db.Column('introduction',db.String(255))
    location = db.Column('location',db.String(255))
    provider = db.Column('provider',db.Integer)

    def __init__(self,bookname , booktype , author,image , introduction,location,provider):
        self.author = author
        self.booktype = booktype
        self.bookname = bookname
        self.author = author
        self.image = image
        self.introduction = introduction
        self.location = location
        self.provider = provider

class Borrower(db.Model):
    __tablename__ = 'borrower'
    booksid = db.Column('booksid',db.Integer,primary_key=True)
    bookname = db.Column('bookname',db.String(255))
    userid = db.Column('userid',db.Integer)
    username = db.Column('username',db.String(255))
    borrowertime = db.Column('borrowertime',db.DateTime,default = datetime.utcnow())

    def __init__(self, bookname, userid, username):
        self.bookname = bookname
        self.userid = userid
        self.username = username

class RankedBooks(db.Model):
    __tablename__ = 'rankedbooks'
    bookname = db.Column('bookname',db.String(255), primary_key=True)
    image = db.Column('image',db.String(255))

    def __init__(self,bookname,image):
        self.bookname = bookname
        self.image = image


class BookMarket(db.Model):
    __tablename__ = 'bookmarket'
    id = db.Column('id',db.Integer,primary_key=True)
    userid = db.Column('userid',db.Integer)
    bookname = db.Column('bookname',db.String(255))
    market = db.Column('market',db.String(255))
    username = db.Column('username',db.String(255))
    time = db.Column('time',db.DateTime,default = datetime.utcnow())

    def __init__(self,userid,bookname,market,username):
        self.userid = userid
        self.bookname = bookname
        self.market = market
        self.username = username