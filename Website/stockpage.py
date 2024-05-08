from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import  login_required, current_user
from .models import Items, Basket, User, Review
from . import db

stockpage = Blueprint('items',__name__)

@stockpage.route('/item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def item(item_id):
    item = Items.query.get_or_404(item_id)
    
    # Retrieve reviews associated with the item
    reviews = Review.query.filter_by(item_id=item_id).all()

    if request.method == 'POST':
        quantity = int(request.form.get('Quantity'))
        basket_item = Basket.query.filter_by(user_id=current_user.id, item_id=item.id).first()

        if basket_item:
            basket_item.quantity += quantity
        else:
            basket_item = Basket(user_id=current_user.id, item_id=item.id, quantity=quantity)
            db.session.add(basket_item)
        
        db.session.commit()
        flash('Item added to basket!', category='success')
        return redirect(url_for('views.home'))

    return render_template('item.html', item=item, reviews=reviews)

@stockpage.route('/submit_review', methods=['POST'])
def submit_review():
    rating = request.form.get('rating')
    comment = request.form.get('opinion')  
    item_id = request.form.get('item_id')

    if not rating or not comment:
        flash('Rating and comment are required.', category='error')
        return redirect(request.referrer)

    rating = int(rating)  # Convert rating to integer

    # Fetch the item based on item_id
    item = Items.query.get(item_id)
    if not item:
        flash('Item not found.', category='error')
        return redirect(request.referrer)

    # Create a new review
    new_review = Review(user_id=current_user.id, item_id=item_id, rating=rating, comment=comment)
    try:
        db.session.add(new_review)
        db.session.commit()
        flash('Review submitted successfully.', category='success')
    except Exception as e:
        flash(f'Failed to submit review due to {str(e)}.', category='error')

    # Redirect the user back to the item page to see the updated reviews
    return redirect(url_for('items.item', item_id=item_id))



