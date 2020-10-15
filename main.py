# Stella Kim
# Assignment 1: Web Frameworks and Flask

import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donor, Donation

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


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
