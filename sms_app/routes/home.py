from flask import Blueprint, render_template, redirect, url_for

home = Blueprint('home', __name__)
      
"""
@home.context_processor
def populate_menu():
    return dict(menu = menu)
"""

@home.route('/home')
def homepage():
    return render_template('home.html')

@home.route('/about')
def aboutpage():
    return render_template('about.html')

@home.route('/contact')
def contactpage():
    return render_template('contact.html')