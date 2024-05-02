from flask import Blueprint, render_template
from flask_login import  login_required, current_user
from .models import Items

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():

    item1 = Items.query.filter_by(name = 'Oak').first()
    item2 = Items.query.filter_by(name = 'Cherry').first()
    item3 = Items.query.filter_by(name = 'Birch').first()
    item4 = Items.query.filter_by(name = 'Jungle').first()

    return render_template("home.html",
                            name1=item1.name,
                            pic1=item1.picture,
                            name2=item2.name,
                            pic2=item2.picture,
                            name3=item3.name,
                            pic3=item3.picture, 
                            name4=item4.name,
                            pic4=item4.picture) #this is the page with all of the items

