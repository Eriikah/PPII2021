from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def home():
    render_template('home.html')