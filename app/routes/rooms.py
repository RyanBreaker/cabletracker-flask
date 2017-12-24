from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models import Room
from app.forms.basic import CreateBasicForm


@app.route('/rooms')
def view_all_rooms():
    rooms = Room.query.all()
    return render_template('room/view_room.html', room=rooms)


@app.route('/rooms/<room_id>')
def view_room(room_id):
    room = Room.query.get_or_404(room_id)
    return render_template('room/view_room.html', room=room)


@app.route('/rooms/create', methods=['GET', 'POST'])
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

    return render_template('room/create_room.html', title='Create Room', form=form)
