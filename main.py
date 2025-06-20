from read import read_products
from write import write_products
from func import display_products, buy_quantity, restock_item


#main function(core of this program) displays the menu
def main():
    products = read_products()
    while True:
        print("\n--- Menu ---")
        print("1. View Products")
        print("2. Purchase products")
        print("3. Restock products")
        print("4. Save and exit")

        choice = input("Choose an option: ")

        if choice == "1":
            display_products(products)

        elif choice == "2":
            buy_quantity(products)
            display_products(products)

        elif choice == "3":
            restock_item(products)
            display_products(products)

        elif choice == "4":
            write_products(products)
            print("Inventory saved. thankyou")
            break

        else:
            print("Invalid choice. Try again.")

#if __name__ == "__main__":  # making sure when the file is run only the main function executes

main()
















