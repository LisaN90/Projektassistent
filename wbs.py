import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, learn
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('wbs', __name__)


@bp.route('/')
def index():
    """Show all the Packages ascending."""
    db = get_db()
    packages = db.execute(
        'SELECT id, nr, name, bac, start_date, end_date'
        ' FROM package'
        ' ORDER BY nr ASC'
    ).fetchall()
    return render_template('wbs/index.html', packages=packages)


def get_package(id):
    """Get a Package
    :return: the Package with information
    :raise 404: if a Package with the given id doesn't exist
    """
    package = get_db().execute(
        'SELECT id, nr, name, bac, start_date, end_date'
        ' FROM package'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if package is None:
        abort(404, "Ein Arbeitspaket mit Nummer {0} existiert nicht.".format(nr))
    return package

@bp.route('/create_package', methods=('GET', 'POST'))
@login_required
def create_package():
    if request.method == 'POST':
        nr = request.form['nr']
        name = request.form['name']
        bac = request.form['bac']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        db = get_db()
        error = None

        if not name:
            error = 'Eine Beschreibung wird benötigt.'
        elif not nr:
            error = 'Eine Arbeitspaketnummer wird benötigt.'
        elif db.execute(
            'SELECT id FROM package WHERE nr = ?', (nr,)
        ).fetchone() is not None:
            error = 'Paket {} existiert bereits.'.format(nr)

        if error is None:
            db.execute(
                'INSERT INTO package (nr, name, bac, start_date, end_date) VALUES ( ?, ?, ?, ?, ?)',
                (nr, name, bac, start_date, end_date)
            )
            db.commit()
            return redirect(url_for('wbs.index'))

        flash(error)

    return render_template('wbs/create_package.html')


@bp.route('/<int:id>/update_package', methods=('GET', 'POST'))
@login_required
def update_package(id):
    package = get_package(id)

    if request.method == 'POST':
        nr = request.form['nr']
        name = request.form['name']
        bac = request.form['bac']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        error = None

        db = get_db()
            
        if not name:
            error = 'Eine Beschreibung wird benötigt.'
        elif not nr:
            error = 'Eine Arbeitspaketnummer wird benötigt.'
        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE package SET nr = ?, name = ?, bac = ?, start_date = ?, end_date = ? WHERE id = ?',
                (nr, name, bac, start_date, end_date, id)
            )
            db.commit()
            return redirect(url_for('wbs.index'))

    return render_template('wbs/update_package.html', package=package)

@bp.route('/<int:id>/delete_package', methods=('POST',))
@login_required
def delete_package(id):
    """Delete a Package"""
    get_package(id)
    db = get_db()
    db.execute('DELETE FROM status WHERE package_id = ?', (id,))
    db.execute('DELETE FROM package WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('wbs.index'))

@bp.route('/<int:id>/create_status', methods=('GET', 'POST'))
@login_required
def create_status(id):
    """Create a new Status for the current user and the Package <id>."""
    if request.method == 'POST':
        title = request.form['title']
        statustext = request.form['statustext']

        text = title + '/' + statustext
        percentage = learn.predict(text)
        error = None

        if not title:
            error = 'Ein Titel wird benötigt.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO status (title, statustext, author_id, package_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, statustext, g.user['id'], id)
            )
            db.commit()
            return redirect(url_for('wbs.index'))

    return render_template('wbs/create_status.html')

@bp.route('/<int:id>/show_status')
def show_status(id):
    package_id = id
    """Show all the Status for one package id ascending."""
    db = get_db()
    statushistory= db.execute(
        'SELECT s.id, u.username, p.nr, p.name, s.created, s.title, '
        '       s.statustext, s.percentage, s.ampel, s.package_id '
        ' FROM status s join user u on s.author_id = u.id'
        '               join package p on s.package_id = p.id'
        ' where s.package_id = ?'
        ' ORDER BY s.id ASC',
        (id,)
    ).fetchall()
    if not statushistory:
        flash('Bisher wurde kein Status zu diesem Arbeitspaket erfasst.')
        return redirect(url_for('wbs.index'))
    else:
        return render_template('wbs/show_status.html', statushistory=statushistory)
