from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"
reviews=[]


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SecretKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_NAME)
    


    db.init_app(app)

    @app.template_filter('currency')
    def currency_filter(value):
        return "£{:,.2f}".format(value)

    from .views import views
    from .auth import auth
    from .payment import payment
    from .stockpage import stockpage

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')  # registering blueprints
    app.register_blueprint(payment, url_prefix='/payment')
    app.register_blueprint(stockpage, url_prefix='/items')


    from .models import User, Basket, Items
    with app.app_context():
        db.create_all()

        create_items()

    @app.route("/items/<int:item_id>")
    def item_details(item_id):
        item = Items.query.get_or_404(item_id)
        return render_template("item.html", item=item)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


   

    return app


def create_items():
        from .models import Items
        # Check if items already exist in the database
        existing_items = Items.query.all()
        if existing_items:
            # Items already exist, no need to add them again
            return


        item1 = Items(name = 'Oak',
                      description = 'This Oak tree gives life to the birds and the bees. It can grow large and old, lasting to up to 800 years!.', 
                      picture = 'oak.png', 
                      price = 12.99, 
                      enviroment_impact = 6)
        
 
        item2 = Items(name = 'Cherry',
                      description = 'This tree is one of a kind! The cherry blossom tree is known for its charm of flowers it blooms.', 
                      picture = 'cherry.jpg', 
                      price = 20.99, 
                      enviroment_impact = 9)


        item3 = Items(name = 'Birch',
                      description = 'Watch its leaves change from vibrant green to striking gold.', 
                      picture = 'birch.jpg', 
                      price = 9.99, 
                      enviroment_impact = 5)
        
    
        item4 = Items(name = 'Jungle',
                      description = 'These hardy trees are ideally suited to exposed, wet land.', 
                      picture = 'jungle.png', 
                      price = 15.99, 
                      enviroment_impact = 4)
        
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.add(item4)


        db.session.commit()
        


