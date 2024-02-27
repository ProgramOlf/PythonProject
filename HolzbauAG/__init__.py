from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from sqlalchemy.sql import text


db = SQLAlchemy()


# Set up logging
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


def create_app():
    app = Flask(__name__)
    import routes
    app.register_blueprint(routes.bp)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SECRET_KEY'] = 'Holzbau'

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Print out the database URI for debugging
    # print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    # Execute a simple SQL query to verify database connection
    #try:
    #    with app.app_context():
    #        result = db.session.execute(text('SELECT 1'))
    #        print("Database Connection Test Result:", result.fetchone())
    #except Exception as e:
    #    print("Error:", e)

    return app