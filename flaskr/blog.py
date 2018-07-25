# Define the blueprint and register it in the application factory

from flask import Blueprint, flash, g, redirect
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


# The /create/ view works the same as the /auth register/ view.
@bp.route('/create', methods=('GET', 'POST'))
# The /login_required/ decorator wrote earlier is used on the blog view.
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.exxecute(
                'INSERT INTO post (title, body, author_id) \
                 VALUES (?, ?, ?)', (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


# Both /update/ and /delete/ views will need to fetch a post by id
#     and check if the author matches the logged in user.
# To avoid duplicating code, we write a func to get the post and call it
#     from each view.
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, create, author_id, username \
         FROM post p JOIN user u ON p.author_id = u.id \
         WHERE p.id = ?',
         (id,)
    ).fetchone()

    if post is None:
        # abort    raise a special exception that returns an HTTP status code.
        abort(404, "Post id {0} doesn't exist.".format(id))
    # check_author     arg is defined so that the func can be used to get
    #                  a post without checking the author.
    if check_author and post['author_id'] != g.user['id']:
        # 403      'Forbidden'
        # 401      'Unauthorized'
        abort(403)

    return post


#
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
# unlike the views u've written so far, the /update/ func takes an arg, id.
# That corresponds to the <int:id> in the route.
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?. body = ?\
                 WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


#
# The /delete/ view doesn't have its own template, the delete button is
# part of update.html and posts to the /<id>/delete URL.
# Since there is no template, it will only handle the POST method then
# redirect to the /index/ view.
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
