# visualizations.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from csv_pandas import read_csv_to_dataframe

def generate_sales_over_time_chart():
    order_data = read_csv_to_dataframe('order_data.csv')

    # Convert the 'Date' column to datetime
    order_data['Date'] = pd.to_datetime(order_data['Date'])

    # Basic statistics
    summary_stats = order_data.describe()

    # Visualizing the total sales over time
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Date', y='Price', data=order_data, estimator='sum')
    plt.title('Total Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')

    # Convert the plot to HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_html = base64.b64encode(buffer.read()).decode('utf-8')

    return chart_html

def generate_furniture_distribution_chart():
    order_data = read_csv_to_dataframe('order_data.csv')

    # Visualizing the distribution of furniture items
    furniture_columns = ['Chair', 'Stool', 'Table', 'Cabinet', 'Dresser', 'Couch', 'Bed', 'Shelf']
    plt.figure(figsize=(12, 8))
    order_data[furniture_columns].sum().plot(kind='bar')
    plt.title('Total Quantity of Each Furniture Item Ordered')
    plt.xlabel('Furniture Items')
    plt.ylabel('Total Quantity')

    # Convert the plot to HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_html = base64.b64encode(buffer.read()).decode('utf-8')

    return chart_html
