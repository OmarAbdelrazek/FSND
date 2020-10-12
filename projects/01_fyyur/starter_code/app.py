#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
from os import name
import dateutil.parser
import babel
from flask import (Flask, 
    render_template, 
    request,   
    Response, 
    flash, redirect, 
    url_for,
    jsonify)
from flask.globals import session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import backref
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.schema import Index
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

from models import app, db, Venue, Artist, Show


app.config.from_object('config')
moment = Moment(app)
db.init_app(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue
  venues = Venue.query.group_by(Venue.id,Venue.city,Venue.state).all()
  visited = []
  data = []
  for venue in venues:
    upcoming_shows_for_venue = Show.query.filter(Show.venue_id == venue.id).filter((Show.start_time > datetime.now())).count()
    if [venue.city,venue.state] not in visited:
      visited.append([venue.city,venue.state])
      data.append(
        {
          "city": venue.city,
          "state": venue.state,
          "venues": [{
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": upcoming_shows_for_venue
          }]
        }
      )
    else:
      index = next((index for (index, d) in enumerate(data) if d["city"] == venue.city and d["state"] == venue.state), None)
      data[index].get("venues").append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": upcoming_shows_for_venue
      })
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_venues = Venue.query.filter(Venue.name.ilike("%"+request.form.get('search_term')+"%")).all()
  data = []
  for venue in search_venues:
    number_of_upcoming_shows = Show.query.filter(Show.start_time > datetime.now()).filter(Show.venue_id == venue.id).count()
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": number_of_upcoming_shows
    })
  response={
    "count": len(search_venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter_by(id = venue_id).first()
  past_shows = db.session.query(Artist,Show).join(Show).join(Venue).filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time < datetime.now()
  ).all()
  upcoming_shows = db.session.query(Artist,Show).join(Show).join(Venue).filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time > datetime.now()
  ).all()
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": (venue.genres),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [{
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(show.start_time)
    }for artist,show in past_shows],
    "upcoming_shows": [{
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": str(show.start_time)
    }for artist, show in upcoming_shows],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  # data = list(filter(lambda d: d['id'] == venue_id, data))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead

  
  try:
      form = VenueForm(request.form)
      venue = Venue()
      form.populate_obj(venue)
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form.get('name') + ' was successfully listed!')
  except:
      flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
      db.session.rollback()
  finally:
      db.session.close()

  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id = venue_id).delete()
    db.session.commit()
    flash('Venue ','was successfully Deleted!')
  except:
    flash('An error occurred. Venue ' + 'could not be Deleted.')
  finally:
    db.session.close()
  

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_result = Artist.query.filter(Artist.name.ilike("%"+request.form.get('search_term')+"%")).all()
  data = []
  for artist in search_result:
    upcoming_shows_for_artist = Show.query.filter(Show.artist_id == artist.id).filter(Show.start_time > datetime.now()).count()
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_of_upcoming_shows": upcoming_shows_for_artist
    })

  response={
    "count": len(search_result),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.filter_by(id = artist_id).first()
  past_shows = db.session.query(Venue, Show).join(Show).join(Artist).filter(
    Show.artist_id == artist_id,
    Show.venue_id == Venue.id,
    Show.start_time < datetime.now()
  ).all()
  upcoming_shows = db.session.query(Venue, Show).join(Show).join(Artist).filter(
    Show.artist_id == artist_id,
    Show.venue_id == Venue.id,
    Show.start_time > datetime.now()
  ).all()
  
  seeking_venue = False
  

  if artist.seeking_venue == True:
    seeking_venue = True
  
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": (artist.genres),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [{
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(show.start_time)
    }for venue,show in past_shows],
    "upcoming_shows": [{
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      "start_time": str(show.start_time)
    }for venue,show in upcoming_shows],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.filter_by(id = artist_id).first()
  artist={
    "id": artist.id,
    "name": artist.name,
    "genres": (artist.genres),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link
    }
  return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  try:
    artist = Artist.query.filter_by(id = artist_id).first()
    form = ArtistForm(request.form)
    form.populate_obj(artist)
    db.session.commit()
    flash('Artist ' + request.form.get('name') + ' was successfully listed!')
  except:
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # TODO: populate form with values from venue with ID <venue_id>
  venue = Venue.query.filter_by(id = venue_id).first()
  venue ={
    'id': venue_id,
    'name': venue.name,
    'genres': venue.genres,
    'address': venue.address,
    'city': venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'website': venue.website,
    'facebook_link': venue.facebook_link,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'image_link': venue.image_link
    }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    venue = Venue.query.filter_by(id = venue_id).first()
    form = VenueForm(request.form)
    form.populate_obj(venue)
    db.session.commit()
    flash('Venue ' + request.form.get('name') + ' was successfully Modified!')
  except:
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be Modified.')
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  try:
    form = ArtistForm(request.form)
    artist = Artist()
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form.get('name') + ' was successfully listed!')
  except:
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  data = []
  for show in shows:
    artist = show.artist
    venue = show.venue
    data.append(
      {
      "venue_id": venue.id,
      "venue_name": venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link, 
      "start_time": str(show.start_time)
      }
    )
  
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    form = ShowForm(request.form)
    show = Show()
    form.populate_obj(show)
    db.session.add(show)
    db.session.commit()
    flash('show ' +  ' was successfully listed!')
  except:
    flash('An error occurred. show ' +  ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()


  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
