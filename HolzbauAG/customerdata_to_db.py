# Extract, transform and load the customer_data.csv into the database

from __init__ import create_app, db
import pandas as pd

# Create the Flask app
app = create_app()

# Load data file
df = pd.read_csv('customer_data.csv')

# Clean Data
df.columns = df.columns.str.strip()

# Import the data into the database using SQLAlchemy
with app.app_context():
    with db.engine.connect() as connection:
        # Fail if table already exists
        df.to_sql('customer_data', connection, if_exists='fail', index=False)