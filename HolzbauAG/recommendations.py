from collections import defaultdict

def generate_recommendations(new_order):
    # Extract relevant data from the new order
    customer_id = new_order.Customer_ID
    chair_count = new_order.Chair
    stool_count = new_order.Stool
    bed_count = new_order.Bed
    dresser_count = new_order.Dresser
    couch_count = new_order.Couch
    table_count = new_order.Table
    
    # Generate recommendations based on the new order
    recommendations = {}

    if chair_count > 2:
        recommendations[customer_id] = "You've purchased more than 2 chairs. Consider adding a table to complete your dining set."
    elif stool_count > 1:
        recommendations[customer_id] = "You've purchased more than 1 stool. Adding another stool or a table could enhance your space."
    elif bed_count > 0 and dresser_count == 0:
        recommendations[customer_id] = "You've purchased a bed but no dresser. A dresser could complement your bedroom setup."
    elif couch_count > 0 and table_count == 0:
        recommendations[customer_id] = "You've purchased a couch but no table. Consider adding a coffee table to complete your living room ensemble."
    else:
        recommendations[customer_id] = "Based on your purchase history, we recommend exploring our wide range of furniture pieces to find your next perfect addition."

    return recommendations
