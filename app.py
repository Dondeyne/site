#!/usr/bin/env python3


from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_babel import Babel, _
from config import *
from os import mkdir, listdir, remove
from os.path import isdir, isfile, join as path_join
from ast import literal_eval


"""
Classes
"""
class Meal():

    def __init__(self, kitchen, name, description = None, image = None):
        self.kitchen     = kitchen
        self.name        = name
        self.description = description
        self.image       = image
        self.save()

    def save(self):
        s = {}
        if self.description:
            s['description'] = self.description
        if self.image:
            s['image'] = self.image
        d = path_join(KITCHEN_MEALS_DIR, self.kitchen)
        if not isdir(d):
            mkdir(d)
        with open(path_join(d, self.name), 'w') as f:
            f.write(str(s))

    def load(kitchen, name):
        d = path_join(KITCHEN_MEALS_DIR, kitchen, name)
        if not isfile(d):
            raise ValueError('') # TODO
        with open(d) as f:
            return Meal(kitchen, name, **literal_eval(f.read()))

    def delete(self):
        remove(path_join(KITCHEN_MEALS_DIR, self.kitchen, self.name))

    def get_all_meals():
        meals = []
        for d in listdir(KITCHEN_MEALS_DIR):
            for f in listdir(path_join(KITCHEN_MEALS_DIR, d)):
                meals.append(Meal.load(d, f))
        return meals


"""
Globals
"""
app = Flask(__name__)
app.secret_key = 'Dit is nodig voor sessions enzo voor de een of andere reden'
app.config.update(dict(
    DEBUG = True,
    LOCALE_PATH = 'translations'
))
babel = Babel(app)


"""
Flask
"""
@babel.localeselector
def get_locale():
    user = getattr(g, 'user', None)
    if user:
        return user.locale
    return request.accept_languages.best_match(['nl', 'fr', 'en'])

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user:
        return user.timezone

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/keuken/')
def get_kitchen_meals():
    return render_template('kitchen.html', meals=Meal.get_all_meals())


@app.route('/keuken/create/')
def get_kitchen_meal_form():
    return render_template('create_meal.html')


@app.route('/keuken/create/', methods=['POST'])
def create_kitchen_meal():
    f = request.form
    if not f.get('kitchen') or not f.get('name'):
        flash(_('Missing kitchen and/or name parameter'), 'error')
        return redirect(url_for('get_kitchen_meal_form'))
    Meal(f.get('kitchen'), f.get('name'), f.get('description'), f.get('image'))
    flash(_('Meal added!'), 'success')
    return redirect(url_for('get_kitchen_meals'))


@app.route('/contact/')
def contact():
    return render_template('contact.html', contacts=CONTACTS)


"""
Run
"""
if __name__ == '__main__':
    if not isdir(KITCHEN_MEALS_DIR):
        mkdir(KITCHEN_MEALS_DIR)
    app.run()
