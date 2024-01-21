import csv
from flask import Blueprint, render_template, request, redirect, url_for
from csv_pandas import read_csv_to_dataframe, write_dataframe_to_csv
import logging
from datetime import datetime


bp = Blueprint('holzbauag', __name__)


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


@bp.route('/')
def home():
    return render_template('index.html', title='HolzbauAG', content='Welcome to HolzbauAG!')


@bp.route('/customer-data', methods=['GET', 'POST'], endpoint='customer_data_route')
def customer_data():
    # Read CSV using pandas
    customer_data = read_csv_to_dataframe('/Users/florianbadura/Desktop/PythonProject/Holzbau AG/data/customer_data.csv')

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
    customer_data = read_csv_to_dataframe('/Users/florianbadura/Desktop/PythonProject/Holzbau AG/data/customer_data.csv')

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
    customer_data = read_csv_to_dataframe('/Users/florianbadura/Desktop/PythonProject/Holzbau AG/data/customer_data.csv')

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
        write_dataframe_to_csv(customer_data, '/Users/florianbadura/Desktop/PythonProject/Holzbau AG/data/customer_data.csv')

        return redirect(url_for('holzbauag.customer_data_route'))

    return redirect(url_for('holzbauag.customer_data_route'))


@bp.route('/order-data', methods=['GET', 'POST'], endpoint='order_data_route')
def order_data():
    # Read CSV using pandas
    order_data = read_csv_to_dataframe('/Users/florianbadura/Desktop/PythonProject/Holzbau AG/data/order_data.csv')

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
    order_data = read_csv_to_dataframe('/Users/florianbadura/Desktop/PythonProject/Holzbau AG/data/order_data.csv')

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
    order_data = read_csv_to_dataframe('/Users/florianbadura/Desktop/PythonProject/Holzbau AG/data/order_data.csv')

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
        write_dataframe_to_csv(order_data, '/Users/florianbadura/Desktop/PythonProject/Holzbau AG/data/order_data.csv')

        return redirect(url_for('holzbauag.order_data_route'))

    return redirect(url_for('holzbauag.order_data_route'))
