from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'SecretKey'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_NAME)

        db.init_app(app)

        @app.template_filter('currency')
        def currency_filter(value):
                return "${:,.2f}".format(value)

        from .views import views
        from .auth import auth
        from .payment import payment
        from .stockpage import stockpage

        app.register_blueprint(views, url_prefix= '/')
        app.register_blueprint(auth, url_prefix= '/auth') #registering blueprints
        app.register_blueprint(payment, url_prefix='/payment')
        app.register_blueprint(stockpage, url_prefix='/items')


        from .models import User, Basket, Items

        

        login_manager = LoginManager()
        login_manager.login_view='auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
                return User.query.get(int(id))

        with app.app_context():
                db.create_all()
                create_items()
        #create_database(app)


        return app

def create_items():
        from .models import Items

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
                      description = 'Embrace the radiant beauty of our yellow flowers. Bask in the warm glow of their vibrant petals, radiating joy and positivity. These blossoms embody the essence of sunshine and happiness, instantly brightening any space they adorn. Their cheerful allure brings a sense of optimism and optimism, infusing your surroundings with a burst of energy. Whether used to create a sunny bouquet or to add a pop of color to your home, these yellow flowers are a delightful symbol of warmth and optimism. Embrace their golden charm and let their sunny disposition uplift your spirits.', 
                      picture = 'birch.jpg', 
                      price = 9.99, 
                      enviroment_impact = 5)
        
    
        item4 = Items(name = 'Jungle',
                      description = 'Experience the enchantment of our exquisite blue flowers. Delicate petals in shades of blue dance with grace, radiating a sense of tranquility and serenity. Embrace their captivating allure and let their stunning hues captivate your senses. Elevate any setting with their timeless beauty, evoking a sense of calm and harmony. Perfect for adding a touch of elegance to any occasion, these blue flowers are sure to leave a lasting impression.', 
                      picture = 'jungle.png', 
                      price = 15.99, 
                      enviroment_impact = 4)
        
        db.session.add(item1)
        db.session.add(item2)
        db.session.add(item3)
        db.session.add(item4)


        db.session.commit()
        


