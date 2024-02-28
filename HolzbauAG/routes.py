import csv
from flask import Blueprint, render_template, request, redirect, url_for , render_template_string, flash, abort
from csv_pandas import read_csv_to_dataframe, write_dataframe_to_csv, find_highest_order_id
import logging
from datetime import datetime
from visualizations import generate_sales_over_time_chart, generate_furniture_distribution_chart,generate_customer_country_chart,generate_customer_age_chart
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, DateField
from wtforms.validators import DataRequired
from __init__ import db
from models import Order, Customer




bp = Blueprint('holzbauag', __name__)




# Create a Class to implement new Order Data
class OrderForm(FlaskForm):
    Order_ID = IntegerField('Order_ID', validators=[DataRequired()])
    Date = DateField('Date', validators=[DataRequired()])
    Customer_ID = IntegerField('Customer_ID', validators=[DataRequired()])
    Price = FloatField('Price', validators=[DataRequired()])
    Chair = IntegerField('Chair', validators=[DataRequired()])
    Stool = IntegerField('Stool', validators=[DataRequired()])
    Table = IntegerField('Table', validators=[DataRequired()])
    Cabinet = IntegerField('Cabinet', validators=[DataRequired()])
    Dresser = IntegerField('Dresser', validators=[DataRequired()])
    Couch = IntegerField('Couch', validators=[DataRequired()])
    Bed = IntegerField('Bed', validators=[DataRequired()])
    Shelf = IntegerField('Shelf', validators=[DataRequired()])
    submit = SubmitField('Submit')




# Create a Class to implement new Customer Data
class CustomerForm(FlaskForm):
    Customer_ID = IntegerField('Customer_ID', validators=[DataRequired()])
    Customer_First_Name = StringField('Customer_First_Name', validators=[DataRequired()])
    Customer_Last_Name = StringField('Customer_Last_Name', validators=[DataRequired()])
    Age = IntegerField('Age', validators=[DataRequired()])
    Country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Submit')




def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data




@bp.route('/')
def home():
    return render_template('index.html',  title='HolzbauAG', content='Welcome to HolzbauAG!')


#########################
# Routes for Order Data #
#########################

@bp.route('/order_data', methods=['GET', 'POST'])
def order_data():
    # Retrieve data from the order_data table
    order_data = Order.query.order_by(Order.Order_ID)
    #print(order_data)  # Check if orders are retrieved
    
    return render_template('order_data.html', 
                           title='Order Data',
                           order_data=order_data)




@bp.route('/add_order_data', methods=['GET', 'POST'])
def add_order_data():
    form = OrderForm()

    # Query the database to find the highest order_id
    highest_order_id = db.session.query(db.func.max(Order.Order_ID)).scalar() or 0
    
    # Increment the highest order_id by one and pass it to the form
    form.Order_ID.data = highest_order_id + 1
    
    if form.validate_on_submit():
        try:
            # Create a new Order instance and add it to the database
            new_order = Order(
                Order_ID=form.Order_ID.data, 
                Date=form.Date.data, 
                Customer_ID=form.Customer_ID.data, 
                Price=form.Price.data,
                Chair=form.Chair.data,
                Stool=form.Stool.data,
                Table=form.Table.data,
                Cabinet=form.Cabinet.data,
                Dresser=form.Dresser.data,
                Couch=form.Couch.data,
                Bed=form.Bed.data,
                Shelf=form.Shelf.data,
            )
            
            db.session.add(new_order)
            db.session.commit()

            # Clear form data
            form.Order_ID.data = highest_order_id + 1  # Increment order ID again
            form.Date.data = ''
            form.Customer_ID.data = ''
            form.Price.data = ''
            form.Chair.data = ''
            form.Stool.data = ''
            form.Table.data = ''
            form.Cabinet.data = ''
            form.Dresser.data = ''
            form.Couch.data = ''
            form.Bed.data = ''
            form.Shelf.data = ''

            # Display a flash message to indicate successful order submission
            flash('Order added successfully!', 'success')

            # Redirect to the order_data2 route to clear the form
            return redirect(url_for('holzbauag.order_data'))
        except Exception as e:
            print(f"Error adding order: {e}")
    else:
        print(form.errors)
        flash('Form validation failed!', 'error')

    return render_template('add_order_data.html', title='Add Order Data', form=form)




@bp.route('/edit_order/<int:Order_ID>', methods=['GET', 'POST'])
def edit_order(Order_ID):
    order = Order.query.get_or_404(Order_ID)
    form = OrderForm()

    if form.validate_on_submit():
        # Update the order object with the form data
        order.Order_ID = form.Order_ID.data
        order.Date = form.Date.data
        order.Customer_ID = form.Customer_ID.data
        order.Price = form.Price.data
        order.Chair = form.Chair.data
        order.Stool = form.Stool.data
        order.Table = form.Table.data
        order.Cabinet = form.Cabinet.data
        order.Dresser = form.Dresser.data
        order.Couch = form.Couch.data
        order.Bed = form.Bed.data
        order.Shelf = form.Shelf.data
    
        # Update the order object with form data
        form.populate_obj(order)  

        # Commit changes to the database
        db.session.commit()

        flash('Order updated successfully!', 'success')
        return redirect(url_for('holzbauag.order_data'))
    else:
        flash('Form validation failed!', 'error')

    return render_template('edit_order.html', form=form, order=order)





@bp.route('/delete_order/<int:order_id>', methods=['GET', 'POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted successfully!', 'success')
    return redirect(url_for('holzbauag.order_data'))





#########################
# Routes for Customer Data #
#########################

@bp.route('/customer_data', methods=['GET', 'POST'])
def customer_data():
    # Retrieve data from the order_data table
    customer_data = Customer.query.order_by(Customer.Customer_ID)
    #print(order_data)  # Check if orders are retrieved
    
    return render_template('customer_data.html', 
                           title='Customer Data',
                           customer_data=customer_data)




@bp.route('/add_customer_data', methods=['GET', 'POST'])
def add_customer_data():
    form = CustomerForm()

    # Query the database to find the highest order_id
    highest_customer_id = db.session.query(db.func.max(Customer.Customer_ID)).scalar() or 0
    
    # Increment the highest order_id by one and pass it to the form
    form.Customer_ID.data = highest_customer_id + 1
    
    if form.validate_on_submit():
        try:
            # Create a new Order instance and add it to the database
            new_customer = Customer(
                Customer_ID=form.Customer_ID.data, 
                Customer_First_Name=form.Customer_First_Name.data, 
                Customer_Last_Name=form.Customer_Last_Name.data, 
                Age=form.Age.data,
                Country=form.Country.data
            )
            
            db.session.add(new_customer)
            db.session.commit()

            # Clear form data
            form.Customer_ID.data = highest_customer_id + 1  # Increment order ID again
            form.Customer_First_Name.data = ''
            form.Customer_Last_Name.data = ''
            form.Age.data = ''
            form.Country.data = ''

            # Display a flash message to indicate successful order submission
            flash('Customer added successfully!', 'success')

            # Redirect to the order_data2 route to clear the form
            return redirect(url_for('holzbauag.customer_data'))
        except Exception as e:
            print(f"Error adding customer: {e}")
    else:
        print(form.errors)
        flash('Form validation failed!', 'error')

    return render_template('add_customer_data.html', title='Add Customer Data', form=form)




@bp.route('/edit_customer/<int:Customer_ID>', methods=['GET', 'POST'])
def edit_customer(Customer_ID):
    customer = Customer.query.get_or_404(Customer_ID)
    form = CustomerForm()

    if form.validate_on_submit():
        # Update the order object with the form data
        customer.Customer_ID = form.Customer_ID.data
        customer.Customer_First_Name = form.Customer_First_Name.data
        customer.Customer_Last_Name = form.Customer_Last_Name.data
        customer.Age = form.Age.data
        customer.Country = form.Country.data
    
        # Update the order object with form data
        form.populate_obj(customer)  

        # Commit changes to the database
        db.session.commit()

        flash('Customer updated successfully!', 'success')
        return redirect(url_for('holzbauag.customer_data'))
    else:
        flash('Form validation failed!', 'error')

    return render_template('edit_customer.html', form=form, customer=customer)





@bp.route('/delete_customer/<int:customer_id>', methods=['GET', 'POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer deleted successfully!', 'success')
    return redirect(url_for('holzbauag.customer_data'))




#############################
# Routes for Visualizations #
#############################

@bp.route('/visualizations', methods=['GET'],endpoint='visualizations_route' )
def visualizations():
    # Generate visualizations
    sales_over_time_chart = generate_sales_over_time_chart()
    furniture_distribution_chart = generate_furniture_distribution_chart()
    customer_country_chart = generate_customer_country_chart()
    customer_age_chart = generate_customer_age_chart()
    # Render the template with the charts
    return render_template('visualizations.html', title='Visualizations',
                           customer_country_chart = customer_country_chart,
                           customer_age_chart = customer_age_chart,
                           sales_over_time_chart=sales_over_time_chart, 
                           furniture_distribution_chart=furniture_distribution_chart)




@bp.route('/Top_10/', methods=['GET', 'POST'])
def top_customer():
    # Query the database to get the required data
    merged_data = db.session.query(Order, Customer).join(Customer, Order.Customer_ID == Customer.Customer_ID).all()

    # Extract relevant data and calculate additional metrics
    merged_data_list = []
    for order, customer in merged_data:
        merged_data_list.append({
            'Customer_ID': customer.Customer_ID,
            'Customer_First_Name': customer.Customer_First_Name,
            'Customer_Last_Name': customer.Customer_Last_Name,
            'Age': customer.Age,
            'Country': customer.Country,
            'Price': order.Price,
            'Chair': order.Chair,
            'Stool': order.Stool,
            'Table': order.Table,
            'Cabinet': order.Cabinet,
            'Dresser': order.Dresser,
            'Couch': order.Couch,
            'Bed': order.Bed,
            'Shelf': order.Shelf
        })

    merged_df = pd.DataFrame(merged_data_list)

    # Calculate additional metrics
    merged_df['Total_Products'] = merged_df[['Chair', 'Stool', 'Table', 'Cabinet', 'Dresser', 'Couch', 'Bed', 'Shelf']].sum(axis=1)

    top_10_products = merged_df.groupby('Customer_ID')['Total_Products'].sum().nlargest(10).reset_index(name='Total_Products')
    top_10_money = merged_df.groupby('Customer_ID')['Price'].sum().nlargest(10).reset_index(name='Total_Spending')

    most_orders_customer_id = merged_df.groupby('Customer_ID')['Total_Products'].sum().idxmax()
    most_spending_customer_id = merged_df.groupby('Customer_ID')['Price'].sum().idxmax()

    top_customer_orders_info = merged_df[merged_df['Customer_ID'] == most_orders_customer_id].copy()
    top_customer_orders_info['Total_Products'] = merged_df[merged_df['Customer_ID'] == most_orders_customer_id]['Total_Products'].sum()

    top_customer_spending_info = merged_df[merged_df['Customer_ID'] == most_spending_customer_id].copy()
    top_customer_spending_info['Total_Spending'] = merged_df[merged_df['Customer_ID'] == most_spending_customer_id]['Price'].sum()

    # Merge with Customer model DataFrame
    # Extracting required columns from the query result
    customers_query_result = Customer.query.with_entities(Customer.Customer_ID, Customer.Customer_First_Name, Customer.Customer_Last_Name, Customer.Age, Customer.Country).all()

    # Constructing DataFrames with required columns
    customers_df = pd.DataFrame(customers_query_result, columns=['Customer_ID', 'Customer_First_Name', 'Customer_Last_Name', 'Age', 'Country'])

    # Merging with top_10_products
    top_10_customers_products = pd.merge(top_10_products, customers_df, on='Customer_ID').sort_values(by='Total_Products', ascending=False)
    
    # Filter the data for the top customer based on most_orders_customer_id
    top_customer_orders_info = merged_df[merged_df['Customer_ID'] == most_orders_customer_id].copy()

    # Calculate the total products for the top customer
    top_customer_total_products = top_customer_orders_info['Total_Products'].sum()

    # Keep only one row for the top customer
    top_customer_orders_info = top_customer_orders_info.iloc[[0]].copy()
    top_customer_orders_info['Total_Products'] = top_customer_total_products

    
    # Merging with top_10_money
    top_10_customers_money = pd.merge(top_10_money, customers_df, on='Customer_ID').sort_values(by='Total_Spending', ascending=False)
    
    # Filter the data for the top spending customer based on most_spending_customer_id
    top_customer_spending_info = merged_df[merged_df['Customer_ID'] == most_spending_customer_id].copy()

    # Calculate the total spending for the top spending customer
    top_customer_total_spending = top_customer_spending_info['Price'].sum()

    # Keep only one row for the top spending customer
    top_customer_spending_info = top_customer_spending_info.iloc[[0]].copy()
    top_customer_spending_info['Total_Spending'] = top_customer_total_spending



    return render_template('Top_10.html',
                           title='Top Customer',
                           top_customer_orders_info=top_customer_orders_info.to_dict(orient='records'),
                           top_customer_spending_info=top_customer_spending_info.to_dict(orient='records'),
                           top_10_customers_products=top_10_customers_products.to_dict(orient='records'),
                           top_10_customers_money=top_10_customers_money.to_dict(orient='records'))




'''
# Task 5
# 8 Marketing campaigns for Holzbau GmbH have been created to activate the customer basis
# 5.1 New Years Marketing Campaign
# Read customer data
customer_data = pd.read_csv('customer_data.csv')

# Extract customer IDs of all customers
all_customer_ids = customer_data['Customer_ID'].unique()

# Send marketing email to all customers
for customer_id in all_customer_ids:
    print(f"Sending marketing email to customer ID {customer_id}:")
    print("Happy New Year from Holzbau!\nStart the year off right with our exclusive New Year's discount event.\nEnjoy up to 30% off on our stylish furniture collections and elevate your home decor for a fresh start in 2024\n")
    

# 5.2 Spring Marketing Campaign
import pandas as pd
# Read customer data
customer_data = pd.read_csv('customer_data.csv')

# Extract customer IDs of all customers
all_customer_ids = customer_data['Customer_ID'].unique()

# Send marketing email to all customers
for customer_id in all_customer_ids:
    print(f"Sending marketing email to customer ID {customer_id}:")
    print("Super spring savings are here!\nComplete your dream home makeover today! Explore our wide selection of stylish furniture pieces at unbeatable prices. Don't miss out – shop now and elevate your living space with comfort and elegance. Use code SPRING24 at checkout for a 30% discount.\n")
 

# 5.3 Special Marketing Strategies per Country
# 5.3.1 USA Marketing Campaign

import pandas as pd

# Load customer data from CSV file
customer_data = pd.read_csv('customer_data.csv')

# Filter customers from the USA
usa_customers = customer_data[customer_data['Country'] == 'USA']

# Print the 4th of July sale message for USA customers
for index, customer in usa_customers.iterrows():
    print("Deck out your home in style this Fourth of July with our spectacular sale at Holzbau GmbH! Celebrate Independence Day with huge discounts on a wide range of furniture, from cozy couches to elegant dining tables. Don't miss this chance to create an inviting space for your family and friends to gather and celebrate! Use code 4JULY at checkout. Happy Shopping!")


# 5.3.2 France Marketing Campaign
import pandas as pd

# Load customer data from CSV file
customer_data = pd.read_csv('customer_data.csv')

# Filter customers from the USA
usa_customers = customer_data[customer_data['Country'] == 'France']

# Print the Bastille day sale message for French customers
for index, customer in usa_customers.iterrows():
    print("Celebrate Bastille day with us!\nEnjoy 30% off on all our furniture to make your home even more beautiful.\nOffer valid only for our customers in France - don't miss out on this special occasion!\n")

# 5.4 Holzbau GmbH's Birthday Marketing Campaign

import pandas as pd

# Read customer data
customer_data = pd.read_csv('customer_data.csv')

# Extract customer IDs of all customers
all_customer_ids = customer_data['Customer_ID'].unique()

# Send marketing email to all customers
for customer_id in all_customer_ids:
    print(f"Sending marketing email to customer ID {customer_id}:")
    print("Join us in celebrating Holzbau GmbH's 20th anniversary!\nTo mark this milestone, we're offering an exclusive 20% discount on all furniture items.\nDon't miss out on this opportunity to spruce up your home with quality pieces at unbeatable prices.\n")
 
# 5.5 Black Friday Marketing Campaign

import pandas as pd

# Read customer data
customer_data = pd.read_csv('customer_data.csv')

# Extract customer IDs of all customers
all_customer_ids = customer_data['Customer_ID'].unique()

# Send marketing email to all customers
for customer_id in all_customer_ids:
    print(f"Sending marketing email to customer ID {customer_id}:")
    print("Black Friday week at Holzbau GmbH\nUnlock unbeatable savings this Black Friday week at Holzbau GmbH!\nFrom luxurious couches to sleek dining sets, indulge in our exclusive discounts and elevate your home decor.\nHurry, seize the opportunity to transform your living space into a haven of style and comfort at prices you won't believe. Up to 50% off. Shop the sale\n")

# 5.6 Christmas Marketing Campaign
# Read customer data
customer_data = pd.read_csv('customer_data.csv')

# Extract customer IDs of all customers
all_customer_ids = customer_data['Customer_ID'].unique()

# Send marketing email to all customers
for customer_id in all_customer_ids:
    print(f"Sending marketing email to customer ID {customer_id}:")
    print("Christmas Sale\nAs the holiday season draws near, we at Holzbau are thrilled to invite you to elevate your festive celebrations with our exquisite furniture offerings.\nFrom cozy sofas to elegant dining sets, we have everything you need to transform your home into a winter wonderland of comfort and style.\nThis Christmas, give the gift of luxury and warmth with our curated selection of timeless pieces.\nWhether you're hosting a grand feast or cozying up by the fireplace, our furniture is designed to create unforgettable moments with your loved ones.\nAs a token of our appreciation for your continued support, we're delighted to offer you an exclusive discount code: XMASJOY20. Use it at checkout to enjoy extra savings on your holiday purchases.\nVisit our website or drop by our showroom to explore our enchanting collection and discover the perfect pieces to make your holiday season truly magical.\n")

# 5.7 Customer Loyalty Marketing Campaign (Email 2 months after their last purchase) 

# 5.8 Customers Sign-Up Birthday Marketing Campaign

# Task 6
import csv

# Understand purchase history
def read_purchase_history(order_data_file):
    purchase_history = {}
    with open(order_data_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Customer_ID = row['Customer_ID']
            purchase_info = {key: int(value) for key, value in row.items() if key != 'Customer ID' and key != 'Date'}
            purchase_history[Customer_ID] = purchase_info
    return purchase_history

# Recommendations for their next purchase
def recommend_next_purchase(purchase_history):
    recommendations = {}
    for Customer_ID, purchases in purchase_history.items():
        chair_count = purchases.get('Chair', 0)
        stool_count = purchases.get('Stool', 0)
        table_count = purchases.get('Table', 0)
        cabinet_count = purchases.get('Cabinet', 0)
        dresser_count = purchases.get('Dresser', 0)
        couch_count = purchases.get('Couch', 0)
        bed_count = purchases.get('Bed', 0)
        shelf_count = purchases.get('Shelf', 0)

        if chair_count > 2:
            recommendations[Customer_ID] = "You've purchased more than 2 chairs. Consider adding a table to complete your dining set."
        elif stool_count > 1:
            recommendations[Customer_ID] = "You've purchased more than 1 stool. Adding another stool or a table could enhance your space."
        elif bed_count > 0 and dresser_count == 0:
            recommendations[Customer_ID] = "You've purchased a bed but no dresser. A dresser could complement your bedroom setup."
        elif couch_count > 0 and table_count == 0:
            recommendations[Customer_ID] = "You've purchased a couch but no table. Consider adding a coffee table to complete your living room ensemble."
        else:
            recommendations[Customer_ID] = "Based on your purchase history, we recommend exploring our wide range of furniture pieces to find your next perfect addition."
    return recommendations

# Purchase history and recommendations
order_data_file = 'order_data.csv'
purchase_history = read_purchase_history(order_data_file)
recommendations = recommend_next_purchase(purchase_history)

# Print recommendations for each customer
for Customer_ID, recommendation in recommendations.items():
    print(f"Customer ID: {Customer_ID}")
    print(f"Recommendation: {recommendation}\n")

 '''   
   
