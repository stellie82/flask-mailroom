# Stella Kim
# Assignment 1: Web Frameworks and Flask

"""Create new donations from existing donors in the database"""

import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session
from model import Donor, Donation, User
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key = b'xm\xdb\xfaJ\xe4\xf4\x9a\x89\x14\xae\xb2(=\xa4\xce\xa4\xa0-\xdc\x86\x1c\xb1\xdf'
# app.secret_key = os.environ.get('SECRET_KEY').encode()


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            user_name = request.form['user']
            user = User.get(User.name == user_name)

            if user and pbkdf2_sha256.verify(request.form['password'],
                                             user.password):
                session['username'] = request.form['user']
                return redirect(url_for('all'))
        except User.DoesNotExist:
            return render_template(
                'login.jinja2', error='Incorrect username or password')
    else:
        return render_template('login.jinja2')


@app.route('/create', methods=['GET', 'POST'])
def create():
    # if request.method == 'GET':
    #     return render_template('create.jinja2')

    if request.method == 'POST':
        try:
            donor_name = request.form['name']  # check DB for existing donor
            donor = Donor.get(Donor.name == donor_name)
        except Donor.DoesNotExist:  # if donor does not exist throw error
            return render_template(
                'create.jinja2', error='DONOR DOES NOT EXIST')

        donation_amount = request.form['amount']  # retrieve donation amount
        donation = Donation(value=donation_amount, donor=donor)
        donation.save()
        return redirect(url_for('all'))
    else:
        return render_template('create.jinja2')


@app.route('/donations')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6738))
    app.run(host='0.0.0.0', port=port)
