## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################


class AlbumEntryForm(FlaskForm):

    aname = StringField("Enter the name of an album:", validators = [Required()])
    arate = RadioField('How much do you like this album? (1 low, 3 high)', choices = [('1', '1'), ('2', '2'), ('3', '3')], validators = [Required()])
    submit = SubmitField('Submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def get_art_form():
    return render_template('artistform.html')

@app.route('/artistlinks')
def linkview():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specificview(artist_name):
    a_dict = {}
    a_dict['term'] = artist_name
    base_url = 'https://itunes.apple.com/search/'
    req = requests.get(base_url, params = a_dict)
    data = json.loads(req.text)
    return render_template('specific_artist.html', results = data['results'])


@app.route('/artistinfo', methods = ['GET'])
def formview():
    artist = request.args.get('artist', '')
    base_url = 'https://itunes.apple.com/search/'
    a_dict = {}
    a_dict['term'] = artist
    req = requests.get(base_url, params = a_dict)
    data = json.loads(req.text)
    return render_template('artist_info.html', objects = data['results'])

@app.route('/album_entry')
def get_alb_form():
    form = AlbumEntryForm()
    return render_template('album_entry.html', form = form)

@app.route('/album_result', methods = ['GET', 'POST'])
def albumformview():
    form = AlbumEntryForm()
    if form.validate_on_submit():
        album = form.aname.data
        rate = form.arate.data
        return render_template('album_data.html', album = album, rate = rate)
    return redirect(url_for('get_alb_form'))

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
