from flask import render_template

from app import app
from app.models import Rack


@app.route('/racks/')
def view_all_racks():
    racks = Rack.query.all()
    return render_template('basic/view_all.html', objects=racks, title='View All Racks')
