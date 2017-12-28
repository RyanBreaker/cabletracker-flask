from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models.tracking import TerminationDeviceType as TermDeviceType
from app.forms.base import BaseForm, BaseDeleteForm

ACTIVE_PAGE = URL_PREFIX = 'termtypes'
LINKS = {
    'create': 'create_termtype',
    'edit': 'edit_termtype',
    'delete': 'delete_termtype',
    'view': 'view_termtype',
    'view_all': 'view_all_termtypes',
}


@app.route('/{}/'.format(URL_PREFIX))
def view_all_termtypes():
    termtypes = TermDeviceType.query.all()
    if len(termtypes) == 0:
        flash('No Termination Device Types exist yet.')
        return redirect(url_for('create_termtype'))
    return render_template('basic/view_all.html', objects=termtypes, links=LINKS,
                           active_page=ACTIVE_PAGE, active_dropdown=LINKS['view_all'])


@app.route('/{}/<object_id>/'.format(URL_PREFIX))
def view_termtype(object_id):
    termtype = TermDeviceType.query.get_or_404(object_id)
    return render_template('basic/view.html', object=termtype, links=LINKS, active_page=ACTIVE_PAGE)


@app.route('/{}/<object_id>/edit/'.format(URL_PREFIX), methods=['GET', 'POST'])
def edit_termtype(object_id):

    termtype = TermDeviceType.query.get_or_404(object_id)
    form = BaseForm(data={'name': termtype.name, 'description': termtype.description})

    if form.validate_on_submit():

        # If name changed
        if termtype.name.lower() != form.name.data.lower():
            if TermDeviceType.query.filter(TermDeviceType.name.ilike(form.name.data)).first() is not None:
                flash('A termination device type with this name already exists.')
                return redirect(url_for('edit_termtype', object_id=object_id))
            termtype.name = form.name.data

        termtype.description = form.description.data
        db.session.commit()
        return redirect(url_for('view_termtype', object_id=termtype.id))

    return render_template('basic/edit.html', form=form, object=termtype, title='Edit Room',
                           links=LINKS, active_page=ACTIVE_PAGE)


@app.route('/{}/create/'.format(URL_PREFIX), methods=['GET', 'POST'])
def create_termtype():

    form = BaseForm()

    if form.validate_on_submit():
        # Get any termtypes of the preexisting name
        termtype = TermDeviceType.query.filter(TermDeviceType.name.ilike(form.name.data)).first()

        if termtype is not None:
            flash('A termination device type with this name already exists.')
            return redirect(url_for('create_termtype'))

        # noinspection PyArgumentList
        termtype = TermDeviceType(name=form.name.data, description=form.description.data)
        db.session.add(termtype)
        db.session.commit()
        return redirect(url_for('view_termtype', object_id=termtype.id))

    return render_template('basic/create.html', title='Create Termination Device Type',
                           form=form, active_page=ACTIVE_PAGE, active_dropdown=LINKS['create'])


@app.route('/{}/<object_id>/delete/'.format(URL_PREFIX), methods=['GET', 'POST'])
def delete_termtype(object_id):

    form = BaseDeleteForm()
    termtype = TermDeviceType.query.get_or_404(object_id)

    if form.validate_on_submit():
        db.session.delete(termtype)
        db.session.commit()
        flash("Termination Device Type '{}' deleted.".format(termtype.name))
        return redirect(url_for('view_all_termtypes'))

    return render_template('basic/delete.html', form=form, links=LINKS, object=termtype)
