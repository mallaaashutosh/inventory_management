import datetime
from read import FILENAME



#function to display products in a formatted way
def display_products(products):
    print("\n" + "=" * 70)
    print(" " * 25 + "PRODUCT INVENTORY")
    print("=" * 70)
    print(f"{'Product ID':20}{'Product Name':20}{'Brand':12}{'Qty':>6}{'Price':>10}{'Origin':>12}{'Total Value':>15}")
    print("-" * 70)
    total_inventory_value = 0
    for item in products:
        total_value = item['quantity'] * item['price']
        total_inventory_value += total_value
        print(
            f"{item['product_id']:20}{item['product_name']:20}{item['brand_name']:12}{item['quantity']:>6}{item['price']:>10.2f}{item['country_of_origin']:>12}{total_value:>15.2f}")
    print("-" * 70)
    print(f"{'Total Inventory Value':>58}{total_inventory_value:>12.2f}")
    print("=" * 70)


#function to restock items
def restock_item(products):  # user input functionality
    restocked_items = []  # this is a temporary list to hold new products for restock
    name_of_vendor = input("Enter vendor's name: ")

    while True:  # this loop keeps asking the user for new product details until user enters done
        product_name = input("Enter product name or if you want to exit enter done")
        if product_name.lower() == 'done':
            break

        brand_name = input("Enter name of the brand: ")
        

        while True:
            try:
                quantity_bought = int(input("Enter Quantity: "))
                if quantity_bought <= 0:
                    print("Quantity must be a positive number.")
                    continue
                break
            except:
                print("Please enter a valid number for quantity.")

        while True:
            try:
                rate_of_item = float(input("Enter Price: "))
                if rate_of_item <= 0:
                    print("price should be a positive number.")
                    continue
                break
            except:
                print("Please enter a valid number for price.")

        # dictionary for new product
        new_product = {
            "product_id": f"{int(datetime.datetime.now().timestamp())}",
            "product_name": product_name,
            "brand_name": brand_name,
            "quantity": quantity_bought,
            "price": rate_of_item,
            "country_of_origin": "Nepal"  # ive set this value default for all new products
        }

        restocked_items.append(new_product)  # appends new product to new_product list
        print("Item added to restock list.")

    if restocked_items:  # checks if at least one item was restocked
        # generates restock invoice for all items
        # calls the invoice functions with values restocked_items and name_of_vendor
        invoice_file = generate_invoice_restock_multiple(restocked_items, name_of_vendor)
        print("restock invoice generated")

        # adds those new items to the main product inventory
        for item in restocked_items:
            products.append(item)  # appends to products
            # writing new items in product-details.txt
            with open(FILENAME, "a") as f:
                f.write(
                    f"{item['product_id']},{item['product_name']},{item['brand_name']},{item['quantity']},{item['price']},{item['country_of_origin']}\n")


    else:
        print("No items were restocked.")


"""
function to generate invoice for restocked products
in this function parameter items refers to list of restocked product dictionary from above 
"""
def generate_invoice_restock_multiple(items, name_of_vendor):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # filename for invoice
    invoice_restock_filename = f"restockinvoice{timestamp}.txt"

    totalCost = 0
    for item in items:  # item is a product and items is a list of products
        totalCost = totalCost + item['quantity'] * item['price']
    vatAmount = round(totalCost * 0.13, 2)
    grandTotal = totalCost + vatAmount

    # multiline formatted doc string for invoice
    invoice = f"""
    ===================================================================================================
    |                                    WeCare Store (Restock Invoice)                                |
    |                                    Ranipauwa, Pokhara-11                                         |
    |==================================================================================================|
    | Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):>60} |
    |==================================================================================================|
    | Product Name      | Brand Name    | Quantity | Rate/Item | Subtotal |
    |--------------------------------------------------------------------------------------------------|
    """
    # looping product in restocked product list
    for item in items:
        subtotal = item['quantity'] * item['price']
        invoice += f"    | {item['product_name']:<15} | {item['brand_name']:<12} | {item['quantity']:>8} | ${item['price']:>8.2f} | ${subtotal:>8.2f} |\n"

    invoice += f"""    |==================================================================================================|
    | Name of Vendor    : {name_of_vendor}
    |==================================================================================================|
    | Subtotal          : ${totalCost:.2f}
    | VAT (13%)         : ${vatAmount:.2f}
    | Grand Total       : ${grandTotal:.2f}
    |==================================================================================================|
    | Thank you for restocking with us!
    ===================================================================================================
    """

    # saving this invoice in a file
    with open(invoice_restock_filename, "w") as f:
        f.write(invoice)
    print(invoice)


def generate_invoice(customer_name, customer_address, purchased_items):
    # this function generates invoice for the customer purchase
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    invoice_filename = f"invoice_{timestamp}.txt"
    
    total_price = sum(item['quantity'] * item['product']['price'] for item in purchased_items)
    vat_amount = round(total_price * 0.13, 2)  # 13% VAT
    grand_total = total_price + vat_amount
    
    invoice = f"""
    ===================================================================================================
    |                                    WeCare Store                                                  |
    |                                    Ranipauwa, Pokhara-11                                         |
    |==================================================================================================|
    | Customer Name: {customer_name:<30} Date: {datetime.datetime.now().strftime('%Y-%m-%d'):>20} |
    | Address: {customer_address:<60} |
    |==================================================================================================|
    | Product ID | Product Name | Brand | Quantity | Free Items | Price/Unit | Total Price |
    |--------------------------------------------------------------------------------------------------|
    """
    
    for item in purchased_items:
        product = item['product']
        total_item_price = item['quantity'] * product['price']
        invoice += f"    | {product['product_id']:<10} | {product['product_name']:<12} | {product['brand_name']:<6} | {item['quantity']:>8} | {item['free']:>10} | ${product['price']:>10.2f} | ${total_item_price:>11.2f} |\n"
    
    invoice += f"""    |==================================================================================================|
    | Subtotal: ${total_price:>85.2f} |
    | VAT (13%): ${vat_amount:>83.2f} |
    | Grand Total: ${grand_total:>80.2f} |
    |==================================================================================================|
    | Thank you for your purchase! |
    ===================================================================================================
    """
    
    with open(invoice_filename, "w") as f:
        f.write(invoice)
    print(invoice)
    
    return invoice_filename


# function handling the purchase
def buy_quantity(products):
    purchased_items = []
    
    # Get customer details first
    while True:
        customer_name = input("Enter your name: ")
        if customer_name.isalpha():
            break
        print("Please enter your name not numbers")
    
    customer_address = input("Enter your address: ")
    
    while True:
        product_name = input("\nEnter product name to buy (or 'done' to finish): ")
        if product_name.lower() == 'done':
            break

        # Find the product
        found_product = None
        for item in products:
            if item["product_name"].lower() == product_name.lower():
                found_product = item
                break
        
        if not found_product:
            print("Product not found. Please enter a valid product name.")
            continue
            
        # Get purchase quantity
        while True:
            try:
                buy_amount = int(input("How many items do you want to purchase? "))
                if buy_amount > 0:
                    break
                print("Please enter a positive number")
            except:
                print("Please enter a valid number")
        
        #Calculate free items and total
        """
        i used the concept of floor division
        in this division if we divide 10 // 3 we get 3(it does not returns point value)
        so customer will get 3 free items if they purchased 10 products
        """
        free = buy_amount // 3
        total_taken = buy_amount + free

        # Check stock
        if found_product["quantity"] < total_taken:
            print(f"Not enough stock for {product_name}. Only {found_product['quantity']} left (including free items).")
            continue
        
        #add to purchase list
        purchased_items.append({
            "product": found_product,
            "quantity": buy_amount,
            "free": free,
            "total_taken": total_taken
        })
        
        # Update stock
        found_product["quantity"] -= total_taken
        print(f"You bought {buy_amount}, get {free} free {total_taken} reduced from stock.")
    
    if purchased_items:
        #generate invoice for all purchased items
        invoice_file = generate_invoice(customer_name, customer_address, purchased_items)
        print(f"Invoice generated: {invoice_file}")
        print("Items purchased successfully and inventory updated.")
        from write import write_products
        write_products(products)
    else:
        print("No items were purchased.")




