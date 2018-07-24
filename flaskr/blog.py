# Define the blueprint and register it in the application factory

from flask import Blueprint, flask, g, redirect
from flask import render_template, request, url_for
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

# unlike the auth bp, the blog bp does not have "url_prefix"
bp = Blueprint('blog', __name__)

# The index will show all of the posts, most recent first.
# A JOIN is used so that the author information from the user table
# is available in the result.
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, \
                created, author_id, username \
         FROM post p JOIN user u ON p.author_id = u.id \
         ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)
