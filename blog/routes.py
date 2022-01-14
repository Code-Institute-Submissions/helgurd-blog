import json
import requests
from flask import render_template
from blog import app


@app.route("/")
def home():
    return render_template("home.html")


# @app.errorhandler(500)
# def internal_error(e):
#     print(e)
#     return render_template('500.html'), 404
#
#
# @app.errorhandler(404)
# def page_not_found(e):
#     print(e)
#     return render_template('404.html'), 404
