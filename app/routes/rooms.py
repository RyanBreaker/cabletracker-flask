from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models import Room
from app.forms.basic import BasicCreateForm


ACTIVE_PAGE = URLPREFIX = 'rooms'


@app.route('/{}/'.format(URLPREFIX))
def view_all_rooms():
    rooms = Room.query.all()
    if len(rooms) == 0:
        flash('No rooms exist yet.')
        return redirect(url_for('create_room'))
    return render_template('basic/view_all.html', objects=rooms, viewlink='view_room',
                           active_page=ACTIVE_PAGE, active_dropdown='view_all_rooms')


@app.route('/{}/<object_id>/'.format(URLPREFIX))
def view_room(object_id):
    room = Room.query.get_or_404(object_id)
    return render_template('basic/view.html', object=room, editlink='edit_room', active_page=ACTIVE_PAGE)


@app.route('/{}/<object_id>/edit/'.format(URLPREFIX), methods=['GET', 'POST'])
def edit_room(object_id):

    room = Room.query.get_or_404(object_id)
    form = BasicCreateForm(data={'name': room.name, 'description': room.description})

    if form.validate_on_submit():

        # If name changed
        if room.name.lower() != form.name.data.lower():
            if Room.query.filter(Room.name.ilike(form.name.data)).first() is not None:
                flash('A room with this name already exists.')
                return redirect(url_for('edit_room', object_id=object_id))
            room.name = form.name.data

        room.description = form.description.data
        db.session.commit()
        return redirect(url_for('view_room', object_id=object_id))

    return render_template('basic/edit.html', form=form, object=room, viewlink='view_room', active_page=ACTIVE_PAGE)


@app.route('/{}/create/'.format(URLPREFIX), methods=['GET', 'POST'])
def create_room():

    form = BasicCreateForm()

    if form.validate_on_submit():
        room = Room.query.filter(Room.name.ilike(form.name.data)).first()

        if room is not None:
            flash('A Room with this name already exists.')
            return redirect(url_for('create_room'))

        # noinspection PyArgumentList
        room = Room(name=form.name.data, description=form.description.data)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('view_room', object_id=room.id))

    return render_template('basic/create.html', title='Create Room', form=form,
                           active_page=ACTIVE_PAGE, active_dropdown='create_room')
