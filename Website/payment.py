from flask import Blueprint, render_template, request,flash, jsonify, redirect
from flask_login import  login_required, current_user
from .models import Basket, Items
from . import db

payment = Blueprint('payment', __name__)

@payment.route('/items/<int:item_id>')
def item_details(item_id):
    item = Items.query.get_or_404(item_id)
    return render_template('item.html', item=item)


@payment.route('/payment', methods = ['GET', 'POST'])
@login_required
def pay():

    if request.method == 'POST':
          CVC = request.form.get('CVC')
          CardNumber = request.form.get('cardnumber')
          DOE = request.form.get('DOE')
          flash('Payment accpeted, thank you', category = 'success')

          # Clear the basket
          Basket.query.filter_by(user_id=current_user.id).delete()
          db.session.commit()

          return render_template('purchased.html') 

    return render_template("payment.html") 

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
                'id': item_detail.id,
                'name': item_detail.name,
                'quantity': basket_item.quantity,
                'price': item_detail.price,
                'total': item_detail.price * basket_item.quantity,
                'picture': item_detail.picture,
            })

    return render_template("basket.html", items=items_with_details, totalprice=totalprice)

@payment.route('/add_to_basket', methods=['POST'])
@login_required
def add_to_basket():
    data = request.json
    item_name = data['item']
    action = data['action']
    item = Items.query.filter_by(name=item_name).first()
    if item:
        basket_item = Basket.query.filter_by(user_id=current_user.id, item_id=item.id).first()
        if basket_item:
            if action == 'add':
                basket_item.quantity += 1
            elif action == 'remove':
                if basket_item.quantity > 1:
                    basket_item.quantity -= 1
                else:
                    db.session.delete(basket_item)
        else:
            if action == 'add':
                new_basketitem = Basket(user_id=current_user.id, item_id=item.id, quantity=1)
                db.session.add(new_basketitem)
    db.session.commit()
    flash('Item added to basket!', category='success')
    return redirect(request.referrer)

@payment.route('/remove_from_basket', methods=['POST'])
@login_required
def remove_from_basket():
    item_name = request.form['item']
    item = Items.query.filter_by(name=item_name).first()
    if item:
        basket_item = Basket.query.filter_by(user_id=current_user.id, item_id=item.id).first()
        if basket_item:
            db.session.delete(basket_item)
            db.session.commit()
            flash('Item removed from basket!', category='success')
            return redirect(request.referrer)
    flash('Item not found in basket!', category='error')
    return redirect(request.referrer)

