import csv
from flask import Blueprint, render_template, request, redirect, url_for , render_template_string
from csv_pandas import read_csv_to_dataframe, write_dataframe_to_csv, find_highest_order_id
import logging
from datetime import datetime
from visualizations import generate_sales_over_time_chart, generate_furniture_distribution_chart


bp = Blueprint('holzbauag', __name__)


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


@bp.route('/')
def home():
    visualizations_url = url_for('holzbauag.visualizations_route')
    return render_template('index.html', title='HolzbauAG', content='Welcome to HolzbauAG!', visualizations_url=visualizations_url)




@bp.route('/customer-data', methods=['GET', 'POST'], endpoint='customer_data_route')
def customer_data():
    # Read CSV using pandas
    customer_data = read_csv_to_dataframe('customer_data.csv')

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'edit':
            selected_row_id = request.form.get('row_id')

            if selected_row_id is not None:
                # Redirect to the edit page with the selected row ID
                return redirect(url_for('holzbauag.edit_customer_row', row_id=selected_row_id))
            else:
                # Handle the case where no row is selected
                return render_template('error.html', error_message='No row selected')

        elif action == 'save_edit':
            # Process the form submission for saving the edited data.
            # Implement the saving logic here.

            # Redirect or render the appropriate page.
            return redirect(url_for('holzbauag.customer_data_route'))
        
    return render_template('customer_data.html', title='Customer Data', data=customer_data)


@bp.route('/edit-customer-row', methods=['POST'], endpoint='edit_customer_row')
def edit_customer_row():
    # Read CSV using pandas
    customer_data = read_csv_to_dataframe('customer_data.csv')

    # Replace this with your logic to get the selected row index
    customer_row_index = request.form.get('selected_row_id', type=int)

    if customer_row_index is None:
        # Handle the case where no row is selected
        logging.error('No row selected')
        return render_template('error.html', error_message='No row selected')

    # Retrieve data for the selected row from your DataFrame
    customer_row_data = customer_data.loc[customer_row_index].tolist()

    # Get the column names to display as headers
    column_names = customer_data.columns.tolist()

    # Debugging statements
    logging.debug(f'Selected Row Index: {customer_row_index}')
    logging.debug(f'Column Names: {column_names}')
    logging.debug(f'Selected Row Data: {customer_row_data}')

    return render_template('edit_customer_row.html', title='Edit Row', customer_row_index=customer_row_index, column_names=column_names, customer_row_data=customer_row_data)


@bp.route('/save-customer-edited-row', methods=['POST'])
def save_customer_edited_row():
    # Read CSV using pandas
    customer_data = read_csv_to_dataframe('customer_data.csv')

    if request.method == 'POST':
        customer_row_index = int(request.form.get('customer_row_index'))

        # Update the selected row data in the DataFrame
        for key in customer_data.columns:
            if key == 'date':  # Replace 'date_column' with the actual date column name
                # Parse the date string into a datetime object
                date_string = request.form.get('date')
                parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
                customer_data.at[customer_row_index, key] = parsed_date
            else:
                customer_data.at[customer_row_index, key] = request.form.get(key)

        # Save the updated DataFrame to CSV
        write_dataframe_to_csv(customer_data, 'customer_data.csv')

        return redirect(url_for('holzbauag.customer_data_route'))

    return redirect(url_for('holzbauag.customer_data_route'))


@bp.route('/order-data', methods=['GET', 'POST'], endpoint='order_data_route')
def order_data():
    # Read CSV using pandas
    order_data = read_csv_to_dataframe('order_data.csv')

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'edit':
            selected_row_id = request.form.get('row_id')

            if selected_row_id is not None:
                # Redirect to the edit page with the selected row ID
                return redirect(url_for('holzbauag.edit_selected_row', row_id=selected_row_id))
            else:
                # Handle the case where no row is selected
                return render_template('error.html', error_message='No row selected')

        elif action == 'save_edit':
            # Process the form submission for saving the edited data.
            # Implement the saving logic here.

            # Redirect or render the appropriate page.
            return redirect(url_for('holzbauag.order_data_route'))

    return render_template('order_data.html', title='Order Data', data=order_data)


@bp.route('/edit-selected-row', methods=['POST'], endpoint='edit_selected_row')
def edit_selected_row():
    # Read CSV using pandas
    order_data = read_csv_to_dataframe('order_data.csv')

    # Replace this with your logic to get the selected row index
    selected_row_index = request.form.get('selected_row_id', type=int)

    if selected_row_index is None:
        # Handle the case where no row is selected
        logging.error('No row selected')
        return render_template('error.html', error_message='No row selected')

    # Retrieve data for the selected row from your DataFrame
    selected_row_data = order_data.loc[selected_row_index].tolist()

    # Get the column names to display as headers
    column_names = order_data.columns.tolist()

    # Debugging statements
    logging.debug(f'Selected Row Index: {selected_row_index}')
    logging.debug(f'Column Names: {column_names}')
    logging.debug(f'Selected Row Data: {selected_row_data}')

    return render_template('edit_selected_row.html', title='Edit Row', selected_row_index=selected_row_index, column_names=column_names, selected_row_data=selected_row_data)


@bp.route('/save-edited-row', methods=['POST'])
def save_edited_row():
    # Read CSV using pandas
    order_data = read_csv_to_dataframe('order_data.csv')

    if request.method == 'POST':
        selected_row_index = int(request.form.get('selected_row_index'))

        # Update the selected row data in the DataFrame
        for key in order_data.columns:
            if key == 'date':  # Replace 'date_column' with the actual date column name
                # Parse the date string into a datetime object
                date_string = request.form.get('date')
                parsed_date = datetime.strptime(date_string, "%Y-%m-%d")
                order_data.at[selected_row_index, key] = parsed_date
            else:
                order_data.at[selected_row_index, key] = request.form.get(key)

        # Save the updated DataFrame to CSV
        write_dataframe_to_csv(order_data, 'order_data.csv')

        return redirect(url_for('holzbauag.order_data_route'))

    return redirect(url_for('holzbauag.order_data_route'))

from flask import render_template

@bp.route('/add-data', methods=['GET', 'POST'])
def add_data():
    # Assuming you have a CSV file named 'order_data.csv'
    file_path = 'order_data.csv'

    # Find the Order_ID with the highest value
    highest_order_id = find_highest_order_id(file_path)

    # Read CSV using the function from the pandas module
    order_data = read_csv_to_dataframe(file_path)

    # Automatically find the highest Order_ID and increment by 1
    highest_order_id = order_data['Order_ID'].astype(int).max() + 1 if not order_data.empty else 1

    if request.method == 'POST':
        # Extract data from the form
        order_id = request.form.get('Order_ID')
        date = request.form.get('date')
        customer_id = request.form.get('customer_id')
        price = request.form.get('price')
        chair = request.form.get('chair')
        stool = request.form.get('stool')
        table = request.form.get('table')
        cabinet = request.form.get('cabinet')
        couch = request.form.get('couch')
        bed = request.form.get('bed')
        shelf = request.form.get('shelf')

        # Check if any field has an input of None
        if None in (order_id, date, customer_id, price, chair, stool, table, cabinet, couch, bed, shelf):
            missing_fields = [field for field, value in {'Order ID': order_id, 'Date': date, 'Customer ID': customer_id, 'Price': price, 'Chair': chair, 'Stool': stool, 'Table': table, 'Cabinet': cabinet, 'Couch': couch, 'Bed': bed, 'Shelf': shelf}.items() if value is None]
            return render_template('add_order_row.html', title='Add Data', missing_fields=missing_fields, highest_order_id=highest_order_id)

        # Convert numeric fields to their respective types
        price = float(price)
        chair = int(chair)
        stool = int(stool)
        table = int(table)
        cabinet = int(cabinet)
        couch = int(couch)
        bed = int(bed)
        shelf = int(shelf)

        # Create a dictionary with the extracted data
        new_data = {
            'Order_ID': highest_order_id,
            'Date': date,
            'Customer_ID': customer_id,
            'Price': float(price),
            'Chair': int(chair),
            'Stool': int(stool),
            'Table': int(table),
            'Cabinet': int(cabinet),
            'Couch': int(couch),
            'Bed': int(bed),
            'Shelf': int(shelf)
        }

        # Append the new_data to the DataFrame
        order_data = order_data.append(new_data, ignore_index=True)

        # Save the updated DataFrame to CSV
        write_dataframe_to_csv(order_data, file_path)

        # Redirect to the order_data_route after adding data
        return redirect(url_for('holzbauag.order_data_route'))

    # Render the page for adding data with the highest Order_ID + 1
    return render_template('add_order_row.html', title='Add Data', highest_order_id=highest_order_id)


@bp.route('/save-new-row', methods=['POST'])
def save_new_row():
    # Read CSV using pandas
    order_data = read_csv_to_dataframe('order_data.csv')

    if request.method == 'POST':
        # Extract data from the form
        order_id = request.form.get('order_id')
        date = request.form.get('date')
        customer_id = request.form.get('customer_id')
        price = request.form.get('price')
        chair = request.form.get('chair')
        stool = request.form.get('stool')
        table = request.form.get('table')
        cabinet = request.form.get('cabinet')
        couch = request.form.get('couch')
        bed = request.form.get('bed')
        shelf = request.form.get('shelf')

        # Check if any field has an input of None
        if None in (order_id, date, customer_id, ...):  # Add other fields as needed
            missing_fields = [field for field, value in {'Order ID': order_id, 'Date': date, 'Customer ID': customer_id, 'Price': price, 'Chair': chair, 'Stool': stool, 'Table': table, 'Cabinet': cabinet, 'Couch': couch, 'Bed': bed, 'Shelf': shelf}.items() if value is None]
            return render_template('add_order_row.html', title='Add Data', missing_fields=missing_fields)

        # Convert numeric fields to their respective types
        price = float(price)
        chair = int(chair)
        stool = int(stool)
        table = int(table)
        cabinet = int(cabinet)
        couch = int(couch)
        bed = int(bed)
        shelf = int(shelf)

        # Create a dictionary with the extracted data
        new_data = {
            'Order_ID': order_id,
            'Date': date,
            'Customer_ID': customer_id,
            'Price': price,
            'Chair': chair,
            'Stool': stool,
            'Table': table,
            'Cabinet': cabinet,
            'Couch': couch,
            'Bed': bed,
            'Shelf': shelf
        }

        # Append the new_data to the DataFrame
        order_data = order_data.append(new_data, ignore_index=True)

        # Save the updated DataFrame to CSV
        write_dataframe_to_csv(order_data, 'order_data.csv')

        # Redirect to the order_data_route after adding data
        return redirect(url_for('holzbauag.order_data_route'))

    # Handle other cases if needed
    return render_template('error.html', error_message='Invalid request')





@bp.route('/visualizations', methods=['GET'],endpoint='visualizations_route' )
def visualizations():
    # Generate visualizations
    sales_over_time_chart = generate_sales_over_time_chart()
    furniture_distribution_chart = generate_furniture_distribution_chart()

    # Render the template with the charts
    return render_template('visualizations.html', title='Visualizations', 
                           sales_over_time_chart=sales_over_time_chart, 
                           furniture_distribution_chart=furniture_distribution_chart)

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
        couch_count = purchases.get('Couche', 0)
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

    
   
