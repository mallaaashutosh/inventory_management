import os

FILENAME = "product-details.txt"  # name of the file where product details are saved and loaded from

def read_products():  # Reads product data from product-details.txt and loads it into a list of dictionaries.
    products = []
    if os.path.exists(FILENAME):  # file exist garxa ki gardena check garxa
        with open(FILENAME, "r") as f:  # opens the file and reads each line
            for line in f:
                line = line.strip()  # splits each line by comma
                if line:  # Skip empty lines
                    try:
                        product_id, product_name, brand_name, quantity, price, country_of_origin = line.split(",")
                        products.append({
                            "product_id": product_id.strip(),
                            "product_name": product_name.strip(),
                            "brand_name": brand_name.strip(),
                            "quantity": int(quantity.strip()),
                            "price": float(price.strip()),
                            "country_of_origin": country_of_origin.strip()
                        })
                    except ValueError:
                        print(f"Warning: Skipping invalid line: {line}")
    return products