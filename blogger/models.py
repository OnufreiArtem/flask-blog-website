from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import datetime 

from blogger import app

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    user_image = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(50))

    def __init__(self, name, surname, username, password):
        self.name = name
        self.surname = surname
        self.user_image = "https://toppng.com/uploads/preview/person-vector-11551054765wbvzeoxz2c.png"
        self.username = username
        self.password = password
    
    def to_json(self):
        return dict(id=self.id, name=self.name, surname=self.surname, username=self.username, user_image=self.user_image, password=self.password) 


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True,  autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
    author = db.Column(db.String(100))
    title = db.Column(db.String(100))
    content = db.Column(db.String(10000))
    date_of_post = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, author_id, title, content):
        self.author_id = author_id
        author_obj = User.query.filter_by(id=author_id).first()
        if author_obj == None:
            self.author = "Unknown"
        else:
            self.author = "%s %s" % (author_obj.name, author_obj.surname)

        self.title = title
        self.content = content
        self.date_of_post = datetime.datetime.now()
    
    def pretty_date(self):
        return date_of_post.strftime("%m/%d/%Y")
db.create_all()
    

