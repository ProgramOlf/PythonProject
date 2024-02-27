# Extract, transform and load the order_data.csv into the database


from __init__ import create_app, db
import pandas as pd

# Create the Flask app
app = create_app()

# Load data file
df = pd.read_csv('order_data.csv')

# Clean Data
df.columns = df.columns.str.strip()

# Convert date column to datetime and then extract the date part
df['Date'] = pd.to_datetime(df['Date']).dt.date

# Import the data into the database using SQLAlchemy
with app.app_context():
    with db.engine.connect() as connection:
        # Fail if table already exists
        df.to_sql('order_data', connection, if_exists='fail', index=False)