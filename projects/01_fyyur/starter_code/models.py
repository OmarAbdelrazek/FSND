from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    name = db.Column(db.String, nullable = False) #done
    city = db.Column(db.String(120), nullable = False) #done
    state = db.Column(db.String(120), nullable = False) #done
    address = db.Column(db.String(120), nullable = False) #done
    phone = db.Column(db.String(120)) #done
    image_link = db.Column(db.String(500)) #done
    facebook_link = db.Column(db.String(120)) #done
    genres = db.Column(db.ARRAY(db.String)) #done
    website = db.Column(db.String(120)) #done
    seeking_talent = db.Column(db.Boolean,default = False) #done
    seeking_description = db.Column(db.String(500)) #done
    show = db.relationship('Show',backref='venue',lazy=True)

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, {self.city}-{self.state},Seeking talent:{self.seeking_talent} "


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True, nullable = False)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String), nullable = False)
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))
    show = db.relationship('Show',backref='artist',lazy=True)

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}"

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer,primary_key = True)
    artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'),nullable = False)
    venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'),nullable=False)
    start_time = db.Column(db.DateTime())

    def __repr__(self) -> str:
        return f"{self.id}, Artist: {self.artist_id}, Venue: {self.venue_id} "
