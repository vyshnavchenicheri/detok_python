import mysql.connector as mysql
import sys

# Establish a database connection
con = mysql.connect(
    host="localhost", 
    user="root", 
    password="123", 
    database="detok_icecream_project"
)
cur = con.cursor()

# Recommendation: Ensure 'Fno' is the PRIMARY KEY in 'OWNERMENUTABLE' for automatic indexing.

# Define a function to generate the next Flavour Number (Fno)
def genFno():
    query = "SELECT max(Fno) FROM ownermenutable"
    cur.execute(query)
    x = cur.fetchone()[0]
    return (x if x is not None else 0)

# Define a function to show available flavors
def show_flavour():
    cur.execute("SELECT * FROM OWNERMENUTABLE")
    print("+------+-----------------+-------+----------+----------+")
    print("| Fno  | Flavor Name     | Rate  | Quantity | Discount |")
    print("+------+-----------------+-------+----------+----------+")
    for row in cur:
        print('| {0:^4} | {1:15} | {2:^5} | {3:^8} | {4:^8} |'.format(row[0], row[1], row[2], row[3], row[4]))
    print("+------+-----------------+-------+----------+----------+")

# Define a function to add a new flavor
def add_flavour():
    Fno = genFno() + 1
    Fname = input('ENTER FLAVOR NAME: ')
    Frate = int(input('ENTER FLAVOR RATE: '))
    Fqty = int(input('ENTER FLAVOR QUANTITY: '))
    Fdis = int(input('ENTER FLAVOR DISCOUNT: '))
    query = "INSERT INTO OWNERMENUTABLE (Fno, Fname, Frate, Fqty, Fdis) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(query, (Fno, Fname, Frate, Fqty, Fdis))
    con.commit()
    print('ITEM ADDED SUCCESSFULLY')

# Define a function to remove a flavor
def remove_flavour():
    Fno = int(input('ENTER FNO OF FLAVOR TO REMOVE: '))
    query = "DELETE FROM OWNERMENUTABLE WHERE Fno = %s"
    cur.execute(query, (Fno,))
    con.commit()
    print('FLAVOR REMOVED')

# Define a function to edit a flavor
def edit_flavour():
    Fno = int(input('ENTER FLAVOR NUMBER OF FLAVOR TO EDIT: '))
    Fname = input('ENTER NEW FLAVOR NAME: ')
    Frate = int(input('ENTER NEW FLAVOR RATE: '))
    Fqty = int(input('ENTER NEW FLAVOR QUANTITY: '))
    Fdis = int(input('ENTER NEW FLAVOR DISCOUNT: '))
    query = "UPDATE OWNERMENUTABLE SET Fname = %s, Frate = %s, Fqty = %s, Fdis = %s WHERE Fno = %s"
    cur.execute(query, (Fname, Frate, Fqty, Fdis, Fno))
    con.commit()
    print('FLAVOR EDITED')

# Define the owner's menu
def owner_menu():
    while True:
        print("\n+------------------------------------------+")
        print("|               OWNER MENU                 |")
        print("+------------------------------------------+")
        print("| (1) ADD FLAVOR                           |")
        print("| (2) SHOW FLAVORS                         |")
        print("| (3) REMOVE A FLAVOR                      |")
        print("| (4) EDIT FLAVOR                          |")
        print("| (5) PREVIOUS MENU                        |")
        print("+------------------------------------------+")
        choice = input("ENTER A CHOICE (1-5): ")
        
        if choice == '1':
            add_flavour()
        elif choice == '2':
            show_flavour()
        elif choice == '3':
            remove_flavour()
        elif choice == '4':
            edit_flavour()
        elif choice == '5':
            break

# Define the customer's menu
def customer_menu():
    cart = {}
    while True:
        print("\n+------------------------------------------+")
        print("|              CUSTOMER MENU               |")
        print("+------------------------------------------+")
        print("| (1) VIEW FLAVORS                         |")
        print("| (2) ADD TO CART                          |")
        print("| (3) VIEW CART                            |")
        print("| (4) MAKE PAYMENT                         |")
        print("| (5) PREVIOUS MENU                        |")
        print("+------------------------------------------+")
        choice = input("ENTER A CHOICE (1-5): ")
        
        if choice == '1':
            show_flavour()
        elif choice == '2':
            fno = int(input("ENTER FLAVOR NUMBER TO ADD TO CART: "))
            fqty = int(input("ENTER QUANTITY: "))
            fname = input("ENTER FLAVOR NAME: ")
            cart[fno] = [fno, fqty, fname]
            print("ADDED TO CART.")
        elif choice == '3':
            print("\n| Fno | Name       | Qty |")
            for item in cart.values():
                print("| {:^3} | {:10} | {:^3} |".format(item[0], item[2], item[1]))
        elif choice == '4':
            total = 0
            print("\n| Fno | Qty | Price |")
            for fno, values in cart.items():
                cur.execute("SELECT Frate FROM OWNERMENUTABLE WHERE Fno = %s", (fno,))
                res = cur.fetchone()
                if res:
                    frate = res[0]
                    subtotal = frate * values[1]
                    total += subtotal
                    print("| {:^3} | {:^3} | ₹{:.2f} |".format(fno, values[1], subtotal))
            print("Total Bill: ₹{:.2f}".format(total))
            payment = input("MAKE PAYMENT (YES/NO): ").strip().lower()
            if payment == "yes":
                print("PAYMENT SUCCESSFUL!")
                cart = {}
            else:
                print("PAYMENT PENDING.")
        elif choice == '5':
            break

# Main menu
while True:
    print("\n+------------------------------------------+")
    print("|          DETOK ICE-CREAM SHOP            |")
    print("+------------------------------------------+")
    print("| (1) OWNER MENU                           |")
    print("| (2) CUSTOMER MENU                        |")
    print("| (3) EXIT                                 |")
    print("+------------------------------------------+")
    choice = input('ENTER A CHOICE (1-3): ')
    if choice == '1':
        owner_menu()
    elif choice == '2':
        customer_menu()
    elif choice == '3':
        con.close()
        sys.exit()
    else:
        print("INVALID CHOICE.")