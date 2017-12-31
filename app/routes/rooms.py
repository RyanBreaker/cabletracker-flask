from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms.base import BaseForm, BaseDeleteForm, name_changed
from app.models.tracking import Room


ACTIVE_PAGE = URLPREFIX = 'rooms'
LINKS = {
    'create': 'create_room',
    'view': 'view_room',
    'view_all': 'view_all_rooms',
    'edit': 'edit_room',
    'delete': 'delete_room',
}


@app.route('/{}/'.format(URLPREFIX))
def view_all_rooms():
    rooms = Room.query.all()
    if len(rooms) == 0:
        flash('No rooms exist yet.')
        return redirect(url_for('create_room'))
    return render_template('basic/view_all.html', objects=rooms, links=LINKS,
                           active_page=ACTIVE_PAGE, active_dropdown='view_all_rooms')


@app.route('/{}/<object_id>/'.format(URLPREFIX))
def view_room(object_id):
    room = Room.query.get_or_404(object_id)
    return render_template('basic/view.html', object=room, links=LINKS, active_page=ACTIVE_PAGE)


@app.route('/{}/<object_id>/edit/'.format(URLPREFIX), methods=['GET', 'POST'])
def edit_room(object_id):

    room = Room.query.get_or_404(object_id)
    form = BaseForm(data={'name': room.name, 'description': room.description})

    if form.validate_on_submit():

        # If name changed
        if name_changed(room.name, form.name.data):
            if Room.name_exists(form.name.data):
                flash('A room with this name already exists.')
                return redirect(url_for('edit_room', object_id=object_id))
            room.name = form.name.data

        room.description = form.description.data
        db.session.commit()
        return redirect(url_for('view_room', object_id=object_id))

    return render_template('basic/edit.html', form=form, object=room, links=LINKS, active_page=ACTIVE_PAGE)


@app.route('/{}/create/'.format(URLPREFIX), methods=['GET', 'POST'])
def create_room():

    form = BaseForm()

    if form.validate_on_submit():

        if Room.name_exists(form.name.data):
            flash('A Room with this name already exists.')
            return redirect(url_for('create_room'))

        # noinspection PyArgumentList
        room = Room(name=form.name.data, description=form.description.data)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('view_room', object_id=room.id))

    return render_template('basic/create.html', title='Create Room', form=form,
                           active_page=ACTIVE_PAGE, active_dropdown='create_room')


@app.route('/{}/<object_id>/delete/'.format(URLPREFIX), methods=['GET', 'POST'])
def delete_room(object_id):

    form = BaseDeleteForm()
    room = Room.query.get_or_404(object_id)

    if form.validate_on_submit():
        db.session.delete(room)
        db.session.commit()
        flash("Room '{}' deleted.".format(room.name))
        return redirect(url_for('view_all_rooms'))

    return render_template('basic/delete.html', form=form, object=room)
