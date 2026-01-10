from read import FILENAME

def write_products(products):  # list of product dictionaries lai product-details.txt ma save garxa.
    with open(FILENAME, "w") as f:  # file lai write mode ma open gareko
        for item in products:  # product ko dictionary lai comma le separate garxa
            f.write(f"{item['product_id']},{item['product_name']},{item['brand_name']},{item['quantity']},{item['price']},{item['country_of_origin']}\n")

