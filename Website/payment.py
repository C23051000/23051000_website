from flask import Blueprint, render_template, request,flash
from flask_login import  login_required, current_user
from .models import Basket, Items


payment = Blueprint('payment', __name__)

@payment.route('/payment', methods = ['GET', 'POST'])
@login_required
def pay():

    if request.method == 'POST':
          CVC = request.form.get('CVC')
          CardNumber = request.form.get('cardnumber')
          DOE = request.form.get('DOE')
          flash('Payment accpeted, thank you', category = 'success')

    return render_template("payment.html") #Payment screen 

@payment.route('/basket')
@login_required
def basket():
    basket_items = Basket.query.filter_by(user_id=current_user.id).all()
    items_with_details = []
    totalprice = 0

    for basket_item in basket_items:
        item_detail = Items.query.filter_by(id=basket_item.item_id).first()
        if item_detail:
            totalprice += item_detail.price * basket_item.quantity
            items_with_details.append({
                'name': item_detail.name,
                'quantity': basket_item.quantity,
                'price': item_detail.price,
                'total': item_detail.price * basket_item.quantity,
                'picture': item_detail.picture,
            })

    return render_template("basket.html", items=items_with_details, totalprice=totalprice)
