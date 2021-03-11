from flask import Flask, render_template, redirect, url_for, g

import models


app = Flask(__name__)
app.run(debug=True, port=8000, host='0.0.0.0')

@app.route('/')
@app.route('/entries')
def listing():


@app.route('/entries/new', methods=('GET', 'POST'))
def create():


@app.route('/entries/<id>', methods=('GET', 'POST'))
def detail(id):


@app.route('/entries/<id>/edit', methods=('GET', 'POST'))
def edit(id):


@app.route('/entries/<id>/delete', methods=('GET', 'POST'))
def delete(id):


