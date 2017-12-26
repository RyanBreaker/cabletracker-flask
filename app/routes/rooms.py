from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models import Room
from app.forms.basic import CreateBasicForm


@app.route('/rooms/')
def view_all_rooms():
    rooms = Room.query.all()
    if len(rooms) == 0:
        flash('No rooms exist yet.')
        return redirect(url_for('create_room'))
    return render_template('rooms/view_all_rooms.html', rooms=rooms)


@app.route('/rooms/<room_id>/')
def view_room(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template('rooms/view_room.html', room=room)


@app.route('/rooms/<room_id>/edit/', methods=['GET', 'POST'])
def edit_room(room_id):

    room = Room.query.get_or_404(room_id)
    form = CreateBasicForm(data={'name': room.name, 'description': room.description})

    if form.validate_on_submit():

        # If name changed
        if room.name.lower() != form.name.data.lower():
            if Room.query.filter(Room.name.ilike(form.name.data)).first() is not None:
                flash('A room with this name already exists.')
                return redirect(url_for('edit_room', room_id=room_id))
            room.name = form.name.data

        room.description = form.description.data
        db.session.commit()
        return redirect(url_for('view_room', room_id=room_id))

    return render_template('rooms/edit_room.html', form=form, room=room)


@app.route('/rooms/create/', methods=['GET', 'POST'])
def create_room():

    form = CreateBasicForm()

    if form.validate_on_submit():
        room = Room.query.filter(Room.name.ilike(form.name.data)).first()

        if room is not None:
            flash('A room with this name already exists.')
            return redirect(url_for('create_room'))

        # noinspection PyArgumentList
        room = Room(name=form.name.data, description=form.description.data)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('view_room', room_id=room.id))

    return render_template('rooms/create_room.html', title='Create Room', form=form)
