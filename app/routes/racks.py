from flask import render_template

from app import app
from app.models.tracking import Rack


URL_PREFIX = 'racks'


@app.route('/{}/'.format(URL_PREFIX))
def view_all_racks():
    racks = Rack.query.all()
    return render_template('basic/view_all.html', objects=racks, title='View All Racks')


@app.route('/{}/create/'.format(URL_PREFIX), methods=['GET', 'POST'])
def create_rack():
    pass


@app.route('/{}/<rack_id>/'.format(URL_PREFIX))
def view_rack(rack_id):
    rack = Rack.query.get_or_404(rack_id)
    print(rack.room)
    return '{}'.format(rack.room)
