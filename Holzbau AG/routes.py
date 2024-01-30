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

    
    
    
    
    
    
   
