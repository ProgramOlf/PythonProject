# visualizations.py

import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from csv_pandas import read_csv_to_dataframe

def generate_sales_over_time_chart():
    order_data = pd.read_csv('order_data.csv', parse_dates=['Date'])

    order_data['Year'] = order_data['Date'].dt.to_period('Y')
    yearly_sales = order_data.groupby('Year')['Price'].sum().reset_index()

    # Convert 'Year' column to string
    yearly_sales['Year'] = yearly_sales['Year'].astype(str)

    # Plotting the total sales for each year
    plt.figure(figsize=(12, 12))
    plt.plot(yearly_sales['Year'], yearly_sales['Price'], marker='o')
    plt.title('Total Sales for Each Year')
    plt.xlabel('Year')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.grid(True)  

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

def generate_customer_country_chart():
    customer_data = read_csv_to_dataframe('customer_data.csv')
    country_counts = customer_data['Country'].value_counts()
    plt.figure(figsize=(8, 6))
    plt.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%', startangle=140, colors = ['#FFD1DC', '#FFA07A', '#CCCCCC', '#FFDEAD', '#B0E0E6', '#98FB98'])
    plt.title('Country Distribution')
    plt.axis('equal')  
    
    
    # Convert the plot to HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_html = base64.b64encode(buffer.read()).decode('utf-8')

    return chart_html
    
def generate_customer_age_chart():
    customer_data = read_csv_to_dataframe('customer_data.csv')
    plt.figure(figsize=(8, 6))
    plt.hist(customer_data['Age'], bins=10, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.title('Age Distribution')
    plt.grid(True)
       

    # Convert the plot to HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_html = base64.b64encode(buffer.read()).decode('utf-8')

    return chart_html