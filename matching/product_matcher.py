def create_fingerprint(row):

    return f"""
Brand: {row['Brand']}
Product: {row['Product_name']}
Color: {row['Colour']}
Description: {row['Description']}
"""