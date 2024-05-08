from Website import create_app
from Website import db  # Import db here

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
    app.run(debug=True)
