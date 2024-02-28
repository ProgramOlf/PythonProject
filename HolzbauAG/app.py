from __init__ import create_app
from models import Order, Customer
from __init__ import db
from datetime import datetime, timedelta

# Create a flask instance from the __init__.py
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)



# 7 Marketing campaigns for Holzbau GmbH have been created to activate the customer basis
# 5.1 New Years Marketing Campaign
# Query all customers from the database
with app.app_context():
    all_customers = Customer.query.all()

# Send marketing email to all customers
for customer in all_customers:
    print(f"Sending marketing email to customer ID {customer.Customer_ID}:")
    print("Happy New Year from Holzbau!\nStart the year off right with our exclusive New Year's discount event.\nEnjoy up to 30% off on our stylish furniture collections and elevate your home decor for a fresh start in 2024\n")

# 5.2 Spring Marketing Campaign
# Query all customers from the database
with app.app_context():
    all_customers = Customer.query.all()

# Send marketing email to all customers
for customer in all_customers:
    print(f"Sending marketing email to customer ID {customer.Customer_ID}:")
    print("Super spring savings are here!\nComplete your dream home makeover today! Explore our wide selection of stylish furniture pieces at unbeatable prices. Don't miss out – shop now and elevate your living space with comfort and elegance. Use code SPRING24 at checkout for a 30% discount.\n")


# 5.3 Special Marketing Strategies per Country
# 5.3.1 USA Marketing Campaign
# Query customers from the USA from the database
with app.app_context():
    usa_customers = Customer.query.filter_by(Country='USA').all()

# Print the 4th of July sale message for USA customers
for customer in usa_customers:
    print("Deck out your home in style this Fourth of July with our spectacular sale at Holzbau GmbH! Celebrate Independence Day with huge discounts on a wide range of furniture, from cozy couches to elegant dining tables. Don't miss this chance to create an inviting space for your family and friends to gather and celebrate! Use code 4JULY at checkout. Happy Shopping!")



# 5.3.2 France Marketing Campaign
# Query customers from the USA from the database
with app.app_context():
    france_customers = Customer.query.filter_by(Country='France').all()

# Print the 4th of July sale message for USA customers
for customer in usa_customers:
    print("Celebrate Bastille day with us!\nEnjoy 30% off on all our furniture to make your home even more beautiful.\nOffer valid only for our customers in France - don't miss out on this special occasion!\n")



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
# Get the current date
current_date = datetime.now().date()

# Define the date for Black Friday (you need to define this date)
black_friday_date = datetime(year=current_date.year, month=11, day=26).date()

# If Black Friday is today, send marketing email
if current_date == black_friday_date:
    # Create the application context
    with app.app_context():
        # Query all customers from the database
        all_customers = Customer.query.all()

        # Send marketing email to all customers
        for customer in all_customers:
            print(f"Sending marketing email to customer ID {customer.Customer_ID}:")
            print("Black Friday week at Holzbau GmbH\nUnlock unbeatable savings this Black Friday week at Holzbau GmbH!\nFrom luxurious couches to sleek dining sets, indulge in our exclusive discounts and elevate your home decor.\nHurry, seize the opportunity to transform your living space into a haven of style and comfort at prices you won't believe. Up to 50% off. Shop the sale\n")

# 5.6 Christmas Marketing Campaign
# Get the current date
current_date = datetime.now().date()

# Check if today is Christmas Eve (December 24th)
if current_date.month == 12 and current_date.day == 24:
    # Create the application context
    with app.app_context():
        # Query all customers from the database
        all_customers = Customer.query.all()

        # Send marketing email to all customers
        for customer in all_customers:
            print(f"Sending marketing email to customer ID {customer.Customer_ID}:")
            print("Christmas Sale\nAs the holiday season draws near, we at Holzbau are thrilled to invite you to elevate your festive celebrations with our exquisite furniture offerings.\nFrom cozy sofas to elegant dining sets, we have everything you need to transform your home into a winter wonderland of comfort and style.\nThis Christmas, give the gift of luxury and warmth with our curated selection of timeless pieces.\nWhether you're hosting a grand feast or cozying up by the fireplace, our furniture is designed to create unforgettable moments with your loved ones.\nAs a token of our appreciation for your continued support, we're delighted to offer you an exclusive discount code: XMASJOY20. Use it at checkout to enjoy extra savings on your holiday purchases.\nVisit our website or drop by our showroom to explore our enchanting collection and discover the perfect pieces to make your holiday season truly magical.\n")

# 5.7 Customer Loyalty Marketing Campaign (Email 2 months after their last purchase) 
# Get the current date
current_date = datetime.now().date()

# Calculate the date two months ago
two_months_ago = current_date - timedelta(days=60)

# Query customers and their last order date from the database
with app.app_context():
    customers_last_order_dates = db.session.query(Customer, db.func.max(Order.Date)).join(Order).group_by(Customer).all()

# Send message to customers whose last order was two months ago or earlier
for customer, last_order_date in customers_last_order_dates:
    if last_order_date and last_order_date <= two_months_ago:
        print(f"Sending message to customer ID {customer.Customer_ID}:")
        print("Dear valued customer,\nIt's been two months since your last purchase with us. We hope you've been enjoying your furniture!\nAs a token of our appreciation, we're pleased to offer you an exclusive discount on your next purchase.\nVisit our website or showroom to explore our latest collections and use code THANKYOU20 at checkout for extra savings.\nWe look forward to serving you again soon!\n")
