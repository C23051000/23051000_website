from flask import Blueprint, render_template, jsonify, request
from flask_login import  login_required, current_user
from .models import Items

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    items = [
            Items.query.filter_by(name='Oak').first(),
            Items.query.filter_by(name='Cherry').first(),
            Items.query.filter_by(name='Birch').first(),
            Items.query.filter_by(name='Jungle').first()
        ]

    return render_template("home.html", items=items)


@views.route('/sort_items')
@login_required
def sort_items():
    criteria = request.args.get('criteria')

    if criteria == 'name':
        items = Items.query.order_by(Items.name).all()
    elif criteria == 'price':
        items = Items.query.order_by(Items.price).all()
    elif criteria == 'environment_impact':
        items = Items.query.order_by(Items.enviroment_impact).all()
    else:
        items = Items.query.all()  # Default sorting

    return render_template("home.html", items=items)


