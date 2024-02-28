import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from __init__ import db
from models import Order, Customer

def generate_sales_over_time_chart():
    # Fetch order data from the database
    orders = db.session.query(Order).all()

    # Convert orders to DataFrame
    order_data = pd.DataFrame([{
        'Date': order.Date,
        'Price': order.Price
    } for order in orders])

    # Group by year and sum up sales
    order_data['Year'] = order_data['Date'].apply(lambda x: x.year)
    yearly_sales = order_data.groupby('Year')['Price'].sum().reset_index()

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
    # Fetch order data from the database
    orders = db.session.query(Order).all()

    # Convert orders to DataFrame
    order_data = pd.DataFrame([{
        'Chair': order.Chair,
        'Stool': order.Stool,
        'Table': order.Table,
        'Cabinet': order.Cabinet,
        'Dresser': order.Dresser,
        'Couch': order.Couch,
        'Bed': order.Bed,
        'Shelf': order.Shelf
    } for order in orders])

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
    # Fetch customer data from the database
    customers = db.session.query(Customer).all()

    # Convert customers to DataFrame
    customer_data = pd.DataFrame([{
        'Country': customer.Country
    } for customer in customers])

    country_counts = customer_data['Country'].value_counts()
    plt.figure(figsize=(8, 6))
    plt.pie(country_counts, labels=country_counts.index, autopct='%1.1f%%', startangle=140, colors = ['#9551CB', '#FFA07A', '#CCCCCC', '#FFDEAD', '#B0E0E6', '#98FB98','#E5F125'])
    plt.title('Country Distribution')
    plt.axis('equal')  

    # Convert the plot to HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_html = base64.b64encode(buffer.read()).decode('utf-8')

    return chart_html
    
def generate_customer_age_chart():
    # Fetch customer data from the database
    customers = db.session.query(Customer).all()

    # Convert customers to DataFrame
    customer_data = pd.DataFrame([{
        'Age': customer.Age
    } for customer in customers])

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
