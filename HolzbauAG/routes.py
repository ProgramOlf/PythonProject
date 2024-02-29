import csv
from flask import Blueprint, render_template, request, redirect, url_for , render_template_string, flash, abort
from csv_pandas import read_csv_to_dataframe, write_dataframe_to_csv, find_highest_order_id
import logging
from datetime import datetime, timedelta
from visualizations import generate_sales_over_time_chart, generate_furniture_distribution_chart,generate_customer_country_chart,generate_customer_age_chart
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, DateField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from __init__ import db
from models import Order, Customer
from collections import defaultdict
from recommendations import generate_recommendations




bp = Blueprint('holzbauag', __name__)




def not_empty(form, field):
    if field.data is None or field.data == '':
        raise ValidationError('This field cannot be empty')




# Custom validator for Customer_ID field
def validate_customer_id(form, field):
    customer_id = field.data
    # Check if customer ID exists in the database
    customer = Customer.query.get(customer_id)
    if not customer:
        raise ValidationError('Customer ID does not exist. Please enter a valid Customer ID.')




# Create a Class to implement new Order Data
class OrderForm(FlaskForm):
    Order_ID = IntegerField('Order_ID', validators=[DataRequired()])
    Date = DateField('Date', validators=[DataRequired()])
    Customer_ID = IntegerField('Customer_ID', validators=[DataRequired(), validate_customer_id])
    Price = FloatField('Price', validators=[DataRequired()])
    Chair = IntegerField('Chair', validators=[not_empty, NumberRange(min=0)])
    Stool = IntegerField('Stool', validators=[not_empty, NumberRange(min=0)])
    Table = IntegerField('Table', validators=[not_empty, NumberRange(min=0)])
    Cabinet = IntegerField('Cabinet', validators=[not_empty, NumberRange(min=0)])
    Dresser = IntegerField('Dresser', validators=[not_empty, NumberRange(min=0)])
    Couch = IntegerField('Couch', validators=[not_empty, NumberRange(min=0)])
    Bed = IntegerField('Bed', validators=[not_empty, NumberRange(min=0)])
    Shelf = IntegerField('Shelf', validators=[not_empty, NumberRange(min=0)])
    submit = SubmitField('Submit')


# Create a Class to implement new Customer Data
class CustomerForm(FlaskForm):
    Customer_ID = IntegerField('Customer_ID', validators=[DataRequired()])
    Customer_First_Name = StringField('Customer_First_Name', validators=[DataRequired()])
    Customer_Last_Name = StringField('Customer_Last_Name', validators=[DataRequired()])
    Age = IntegerField('Age', validators=[DataRequired()])
    Country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Submit')





# Display of the homepage
@bp.route('/')
def home():
    return render_template('index.html',  title='HolzbauAG', content='Welcome to HolzbauAG!', content2='Navigate the page to work with the customer and order data.', content3 ='Additionally, you can analyse the data in Top Customers and visualize data in Visualizations!')


#########################
# Routes for Order Data #
#########################

# Display the Order Data
@bp.route('/order_data', methods=['GET', 'POST'])
def order_data():
    # Retrieve data from the order_data table
    order_data = Order.query.order_by(Order.Order_ID)
    #print(order_data)  # Check if orders are retrieved
    
    return render_template('order_data.html', 
                           title='Order Data',
                           order_data=order_data)




# Adding of Order Data in a new webpage using forms
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

            # Generate recommendations based on the new order
            recommendations = generate_recommendations(new_order)

            # Concatenate recommendations into a single message
            recommendation_message = "<br>".join(recommendations.values())

            # Display a flash message with recommendations
            flash(recommendation_message, 'info')

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

            # Redirect to the order_data route to clear the form
            return redirect(url_for('holzbauag.order_data'))
        except Exception as e:
            print(f"Error adding order: {e}")
            flash('Error adding order. Please try again later.', 'error')
    else:
        print(form.errors)

    return render_template('add_order_data.html', title='Add Order Data', form=form)







# Editing existing Data in a new webpage using forms
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

    return render_template('edit_order.html', form=form, order=order)





# Deletion of Data inside the Edit Order Data Page
@bp.route('/delete_order/<int:order_id>', methods=['GET', 'POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted successfully!', 'success')
    return redirect(url_for('holzbauag.order_data'))





############################
# Routes for Customer Data #
############################

# Display the Order Data
@bp.route('/customer_data', methods=['GET', 'POST'])
def customer_data():
    # Retrieve data from the order_data table
    customer_data = Customer.query.order_by(Customer.Customer_ID)
    #print(order_data)  # Check if orders are retrieved
    
    return render_template('customer_data.html', 
                           title='Customer Data',
                           customer_data=customer_data)




# Adding of Order Data in a new webpage using forms
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

    return render_template('add_customer_data.html', title='Add Customer Data', form=form)




# Editing existing Data in a new webpage using forms
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

    return render_template('edit_customer.html', form=form, customer=customer)





# Deletion of Data inside the Edit Customer Data Page
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




############################
# Routes for Top Customers #
############################

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




##########
# Task 5 #
##########
'''
# 7 Marketing campaigns for Holzbau GmbH have been created to activate the customer basis
# 5.1 New Years Marketing Campaign
# Query all customers from the database
all_customers = Customer.query.all()

# Send marketing email to all customers
for customer in all_customers:
    print(f"Sending marketing email to customer ID {customer.Customer_ID}:")
    print("Happy New Year from Holzbau!\nStart the year off right with our exclusive New Year's discount event.\nEnjoy up to 30% off on our stylish furniture collections and elevate your home decor for a fresh start in 2024\n")

# 5.2 Spring Marketing Campaign
# Query all customers from the database
all_customers = Customer.query.all()

# Send marketing email to all customers
for customer in all_customers:
    print(f"Sending marketing email to customer ID {customer.Customer_ID}:")
    print("Super spring savings are here!\nComplete your dream home makeover today! Explore our wide selection of stylish furniture pieces at unbeatable prices. Don't miss out – shop now and elevate your living space with comfort and elegance. Use code SPRING24 at checkout for a 30% discount.\n")


# 5.3 Special Marketing Strategies per Country
# 5.3.1 USA Marketing Campaign
# Query customers from the USA from the database
usa_customers = Customer.query.filter_by(Country='USA').all()

# Print the 4th of July sale message for USA customers
for customer in usa_customers:
    print("Deck out your home in style this Fourth of July with our spectacular sale at Holzbau GmbH! Celebrate Independence Day with huge discounts on a wide range of furniture, from cozy couches to elegant dining tables. Don't miss this chance to create an inviting space for your family and friends to gather and celebrate! Use code 4JULY at checkout. Happy Shopping!")



# 5.3.2 France Marketing Campaign
# Query customers from the USA from the database
usa_customers = Customer.query.filter_by(Country='USA').all()

# Print the 4th of July sale message for USA customers
for customer in usa_customers:
    print("Celebrate Bastille day with us!\nEnjoy 30% off on all our furniture to make your home even more beautiful.\nOffer valid only for our customers in France - don't miss out on this special occasion!\n")

# 5.4 Holzbau GmbH's Birthday Marketing Campaign
# Get the current date
current_date = datetime.now().date()

# Query customers with a birthday today from the database
customers_with_birthday_today = Customer.query.filter(
    db.extract('month', Customer.birthdate) == current_date.month,
    db.extract('day', Customer.birthdate) == current_date.day
).all()

# Send marketing email to customers with a birthday today
for customer in customers_with_birthday_today:
    print(f"Sending marketing email to customer ID {customer.Customer_ID}:")
    print("Happy Birthday from Holzbau GmbH!\nWishing you a fantastic day filled with joy and happiness. As a token of our appreciation, enjoy a special birthday discount on your next purchase!\n")

# 5.5 Black Friday Marketing Campaign
# Get the current date
current_date = datetime.now().date()

# Calculate the date of Black Friday for the current year
year = current_date.year
black_friday_date = None

# Black Friday is the fourth Friday of November
for day in range(23, 30):
    date = datetime(year, 11, day)
    if date.weekday() == 4:  # Friday
        black_friday_date = date
        break

# If Black Friday is today, send marketing email
if current_date == black_friday_date:
    # Read customer data
    customer_data = pd.read_csv('customer_data.csv')

    # Extract customer IDs of all customers
    all_customer_ids = customer_data['Customer_ID'].unique()

    # Send marketing email to all customers
    for customer_id in all_customer_ids:
        print(f"Sending marketing email to customer ID {customer_id}:")
        print("Black Friday week at Holzbau GmbH\nUnlock unbeatable savings this Black Friday week at Holzbau GmbH!\nFrom luxurious couches to sleek dining sets, indulge in our exclusive discounts and elevate your home decor.\nHurry, seize the opportunity to transform your living space into a haven of style and comfort at prices you won't believe. Up to 50% off. Shop the sale\n")

# 5.6 Christmas Marketing Campaign
# Get the current date
current_date = datetime.now().date()

# Check if today is Christmas Eve (December 24th)
if current_date.month == 12 and current_date.day == 24:
    # Read customer data
    customer_data = pd.read_csv('customer_data.csv')

    # Extract customer IDs of all customers
    all_customer_ids = customer_data['Customer_ID'].unique()

    # Send marketing email to all customers
    for customer_id in all_customer_ids:
        print(f"Sending marketing email to customer ID {customer_id}:")
        print("Christmas Sale\nAs the holiday season draws near, we at Holzbau are thrilled to invite you to elevate your festive celebrations with our exquisite furniture offerings.\nFrom cozy sofas to elegant dining sets, we have everything you need to transform your home into a winter wonderland of comfort and style.\nThis Christmas, give the gift of luxury and warmth with our curated selection of timeless pieces.\nWhether you're hosting a grand feast or cozying up by the fireplace, our furniture is designed to create unforgettable moments with your loved ones.\nAs a token of our appreciation for your continued support, we're delighted to offer you an exclusive discount code: XMASJOY20. Use it at checkout to enjoy extra savings on your holiday purchases.\nVisit our website or drop by our showroom to explore our enchanting collection and discover the perfect pieces to make your holiday season truly magical.\n")

# 5.7 Customer Loyalty Marketing Campaign (Email 2 months after their last purchase) 
# Get the current date
current_date = datetime.now().date()

# Calculate the date two months ago
two_months_ago = current_date - timedelta(days=60)

# Query customers and their last order date from the database
customers_last_order_dates = db.session.query(Customer, db.func.max(Order.Date)).join(Order).group_by(Customer).all()

# Send message to customers whose last order was two months ago or earlier
for customer, last_order_date in customers_last_order_dates:
    if last_order_date and last_order_date <= two_months_ago:
        print(f"Sending message to customer ID {customer.Customer_ID}:")
        print("Dear valued customer,\nIt's been two months since your last purchase with us. We hope you've been enjoying your furniture!\nAs a token of our appreciation, we're pleased to offer you an exclusive discount on your next purchase.\nVisit our website or showroom to explore our latest collections and use code THANKYOU20 at checkout for extra savings.\nWe look forward to serving you again soon!\n")
'''
