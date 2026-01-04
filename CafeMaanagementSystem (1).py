import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import os
import webbrowser

# File names for data storage
MENU_FILE = "cafe_menu.txt"
ORDERS_FILE = "cafe_orders.txt"
INVENTORY_FILE = "cafe_inventory.txt"

# Global variables
current_order_items = []
current_order_total = 0.0
order_counter = 1


# Initialize files if they don't exist
def initialize_files():
    # Menu file
    if not os.path.exists(MENU_FILE):
        with open(MENU_FILE, "w") as file:
            file.write("Coffee,50\nTea,30\nSandwich,120\nCake,80\nBurger,150\nFries,60\nJuice,70\nWater,20\n")

    # Orders file
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "w") as file:
            file.write("")

    # Inventory file
    if not os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, "w") as file:
            file.write("Coffee,100\nTea,100\nSandwich,50\nCake,30\nBurger,50\nFries,80\nJuice,60\nWater,100\n")


# Load menu from file
def load_menu():
    menu_items = {}
    try:
        with open(MENU_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) >= 2:
                        item_name = parts[0].strip()
                        price = float(parts[1].strip())
                        menu_items[item_name] = price
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load menu: {e}")
    return menu_items


# Load inventory from file
def load_inventory():
    inventory = {}
    try:
        with open(INVENTORY_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) >= 2:
                        item_name = parts[0].strip()
                        quantity = int(parts[1].strip())
                        inventory[item_name] = quantity
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load inventory: {e}")
    return inventory


# Save inventory to file
def save_inventory(inventory):
    try:
        with open(INVENTORY_FILE, "w") as file:
            for item, quantity in inventory.items():
                file.write(f"{item},{quantity}\n")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save inventory: {e}")
        return False


# Save order to file
def save_order(order_id, customer_name, items, total_amount, status):
    try:
        with open(ORDERS_FILE, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            items_str = ";".join([f"{item['name']}:{item['quantity']}:{item['price']}" for item in items])
            file.write(f"{order_id},{timestamp},{customer_name},{items_str},{total_amount},{status}\n")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save order: {e}")
        return False


# Load orders from file
def load_orders():
    orders = []
    try:
        with open(ORDERS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) >= 6:
                        order_id = parts[0].strip()
                        timestamp = parts[1].strip()
                        customer_name = parts[2].strip()
                        items_str = parts[3].strip()
                        total_amount = float(parts[4].strip())
                        status = parts[5].strip()

                        # Parse items
                        items = []
                        if items_str:
                            item_parts = items_str.split(";")
                            for item_part in item_parts:
                                item_details = item_part.split(":")
                                if len(item_details) >= 3:
                                    item_name = item_details[0]
                                    quantity = int(item_details[1])
                                    price = float(item_details[2])
                                    items.append({
                                        "name": item_name,
                                        "quantity": quantity,
                                        "price": price
                                    })

                        orders.append({
                            "id": order_id,
                            "timestamp": timestamp,
                            "customer": customer_name,
                            "items": items,
                            "total": total_amount,
                            "status": status
                        })
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load orders: {e}")
    return orders


# Generate QR Code for payment
def generate_qr_code():
    """Generate a QR code for the current order total"""
    if not current_order_items:
        messagebox.showwarning("Warning", "No items in the order. Please add items first.")
        return

    # Create QR code window
    qr_window = tk.Toplevel()
    qr_window.title("Payment QR Code")
    qr_window.geometry("400x500")

    # Generate a unique transaction ID
    transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Create payment details
    payment_amount = current_order_total
    payment_text = f"""
    CAFE BILL PAYMENT

    Transaction ID: {transaction_id}
    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    Total Amount: PKR {payment_amount:.2f}

    Please scan to pay

    Payment Methods:
    • JazzCash
    • EasyPaisa
    • Bank Transfer
    • Cash

    Thank you for your payment!
    """

    # Create QR code text display
    qr_frame = tk.Frame(qr_window)
    qr_frame.pack(pady=20)

    # Create a simple ASCII QR code representation
    # Note: For actual QR code generation, you would need to install qrcode library
    # pip install qrcode[pil]

    # Display payment information
    info_label = tk.Label(qr_frame, text="=== PAYMENT QR CODE ===", font=("Courier", 12, "bold"))
    info_label.pack()

    # Create a simple QR code representation (ASCII art)
    qr_display = tk.Text(qr_window, width=40, height=15, font=("Courier", 8))
    qr_display.pack(padx=20, pady=10)

    # Generate simple QR pattern (ASCII representation)
    qr_pattern = """
    ██████████████    ██  ██████████████
    ██          ██    ██  ██          ██
    ██  ██████  ██    ██  ██  ██████  ██
    ██  ██████  ██        ██  ██████  ██
    ██  ██████  ██    ██  ██  ██████  ██
    ██          ██    ██  ██          ██
    ██████████████  ██  ██████████████
            ██      ██  ██      ██    
    ██  ██  ██  ██    ██  ██  ██  ██  ██
        ██      ██  ██      ██  ██    
    ██████  ██  ██  ██  ██  ██  ██████
    ██    ██      ██  ██      ██    ██
        ██  ██  ██    ██  ██  ██  ██  
    ██  ██      ██  ██      ██  ██  ██
    ██    ██  ██  ██  ██  ██  ██    ██
            ██  ██    ██  ██  ██      
    ██████████████  ██  ██████████████
    ██          ██    ██  ██          ██
    ██  ██████  ██        ██  ██████  ██
    ██  ██████  ██    ██  ██  ██████  ██
    ██  ██████  ██    ██  ██  ██████  ██
    ██          ██    ██  ██          ██
    ██████████████  ██  ██████████████
    """

    qr_display.insert(tk.END, qr_pattern)
    qr_display.insert(tk.END, "\n" + "=" * 40 + "\n")
    qr_display.insert(tk.END, payment_text)
    qr_display.config(state='disabled')

    # Add payment instructions
    instructions = tk.Label(qr_window, text="Scan QR code with your mobile banking app",
                            font=("Arial", 10, "italic"))
    instructions.pack(pady=5)

    # Add payment methods
    methods_label = tk.Label(qr_window, text="Available Payment Methods:", font=("Arial", 10, "bold"))
    methods_label.pack(pady=5)

    methods_frame = tk.Frame(qr_window)
    methods_frame.pack()

    # Create buttons for different payment methods
    def open_jazzcash():
        webbrowser.open("https://www.jazzcash.com.pk/")

    def open_easypaisa():
        webbrowser.open("https://www.easypaisa.com.pk/")

    tk.Button(methods_frame, text="JazzCash", command=open_jazzcash, bg="#FF6B00", fg="white", width=12).grid(row=0,
                                                                                                              column=0,
                                                                                                              padx=5)
    tk.Button(methods_frame, text="EasyPaisa", command=open_easypaisa, bg="#00A859", fg="white", width=12).grid(row=0,
                                                                                                                column=1,
                                                                                                                padx=5)

    # Add buttons
    button_frame = tk.Frame(qr_window)
    button_frame.pack(pady=10)

    def print_receipt():
        """Print a simple receipt"""
        receipt_text = f"""
        CAFE RECEIPT
        ======================
        Transaction ID: {transaction_id}
        Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ----------------------
        Items:
        """
        for item in current_order_items:
            receipt_text += f"{item['name']} x{item['quantity']}: PKR {item['total']:.2f}\n"

        receipt_text += f"""
        ----------------------
        Total: PKR {payment_amount:.2f}
        ======================
        Thank you for your payment!
        """

        # Show receipt in a new window
        receipt_window = tk.Toplevel()
        receipt_window.title("Payment Receipt")
        receipt_window.geometry("400x400")

        receipt_display = scrolledtext.ScrolledText(receipt_window, width=45, height=20)
        receipt_display.pack(padx=10, pady=10)
        receipt_display.insert(tk.END, receipt_text)
        receipt_display.config(state='disabled')

        tk.Button(receipt_window, text="Close", command=receipt_window.destroy,
                  bg="#f44336", fg="white", width=15).pack(pady=10)

    tk.Button(button_frame, text="Print Receipt", command=print_receipt,
              bg="#2196F3", fg="white", width=15).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Close", command=qr_window.destroy,
              bg="#f44336", fg="white", width=15).grid(row=0, column=1, padx=5)

    # Update order status to "Paid" if user confirms
    def mark_as_paid():
        if messagebox.askyesno("Confirm Payment", "Mark this order as paid?"):
            # In a real system, you would update the order status in the database
            messagebox.showinfo("Success", "Payment recorded successfully!")
            qr_window.destroy()

    tk.Button(qr_window, text="Mark as Paid", command=mark_as_paid,
              bg="#4CAF50", fg="white", width=20).pack(pady=10)


# Simple login function
def login():
    # Create login window
    login_window = tk.Tk()
    login_window.title("Cafe Login")
    login_window.geometry("300x200")
    login_window.configure(bg="#f0f0f0")

    # Make window not resizable
    login_window.resizable(False, False)

    # Title
    title_label = tk.Label(login_window, text="Cafe Management System",
                           font=("Arial", 14, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)

    # Login label
    login_label = tk.Label(login_window, text="Login",
                           font=("Arial", 12), bg="#f0f0f0")
    login_label.pack(pady=5)

    # Username
    username_label = tk.Label(login_window, text="Username:", bg="#f0f0f0")
    username_label.pack()

    username_entry = tk.Entry(login_window, width=25)
    username_entry.pack(pady=5)
    username_entry.focus()

    # Password
    password_label = tk.Label(login_window, text="Password:", bg="#f0f0f0")
    password_label.pack()

    password_entry = tk.Entry(login_window, width=25, show="*")
    password_entry.pack(pady=5)

    # Login button function
    def check_login():
        username = username_entry.get()
        password = password_entry.get()

        # Simple username and password check
        if username == "admin" and password == "admin123":
            login_window.destroy()
            main()
        elif username == "staff" and password == "staff123":
            login_window.destroy()
            main()
        else:
            messagebox.showerror("Login Failed", "Wrong username or password!")
            password_entry.delete(0, tk.END)
            username_entry.focus()

    # Login button
    login_button = tk.Button(login_window, text="Login",
                             command=check_login, bg="#4CAF50", fg="white",
                             width=15)
    login_button.pack(pady=10)

    # Bind Enter key to login
    def on_enter(event):
        check_login()

    login_window.bind('<Return>', on_enter)

    # Info label
    info_label = tk.Label(login_window,
                          text="Use: admin/admin123 or staff/staff123",
                          font=("Arial", 8), bg="#f0f0f0", fg="blue")
    info_label.pack(pady=5)

    login_window.mainloop()


# Main application
def main():
    # Initialize data files
    initialize_files()

    # Load data
    menu_items = load_menu()
    inventory = load_inventory()
    orders = load_orders()

    # Global variables
    global current_order_items
    global current_order_total
    global order_counter

    order_counter = len(orders) + 1

    # Create main window
    root = tk.Tk()
    root.title("Simple Cafe Management System")
    root.geometry("900x700")
    root.configure(bg="#f0f0f0")

    # Functions for the application

    def update_menu_display():
        """Update the menu display in the GUI"""
        menu_text.delete(1.0, tk.END)
        for item, price in menu_items.items():
            stock = inventory.get(item, 0)
            menu_text.insert(tk.END, f"{item:20} PKR {price:6.2f}  (Stock: {stock})\n")

    def update_order_display():
        """Update the current order display in the GUI"""
        order_text.delete(1.0, tk.END)
        if not current_order_items:
            order_text.insert(tk.END, "No items in the order.\n")
            return

        for item in current_order_items:
            order_text.insert(tk.END, f"{item['name']} x{item['quantity']} = PKR {item['total']:.2f}\n")

        order_text.insert(tk.END, f"\n{'Total:':25} PKR {current_order_total:.2f}")

    def add_to_order():
        """Add selected item to the current order"""
        global current_order_total
        global current_order_items

        selected_item = item_var.get()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item from the menu.")
            return

        try:
            quantity = int(quantity_var.get())
            if quantity <= 0:
                messagebox.showwarning("Warning", "Quantity must be greater than 0.")
                return
        except:
            messagebox.showwarning("Warning", "Please enter a valid quantity.")
            return

        # Check inventory
        if selected_item in inventory and inventory[selected_item] < quantity:
            messagebox.showwarning("Warning", f"Not enough stock. Only {inventory[selected_item]} available.")
            return

        # Add to order
        price = menu_items[selected_item]
        item_total = price * quantity

        # Check if item already in order
        item_found = False
        for item in current_order_items:
            if item['name'] == selected_item:
                item['quantity'] += quantity
                item['total'] = item['price'] * item['quantity']
                item_found = True
                break

        if not item_found:
            current_order_items.append({
                'name': selected_item,
                'price': price,
                'quantity': quantity,
                'total': item_total
            })

        # Update total
        current_order_total = 0.0
        for item in current_order_items:
            current_order_total += item['total']

        # Update displays
        update_order_display()

        # Reset quantity
        quantity_var.set("1")

    def remove_from_order():
        """Remove selected item from the current order"""
        global current_order_total
        global current_order_items

        selected_item = item_var.get()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item from the menu.")
            return

        # Find and remove the item
        for i, item in enumerate(current_order_items):
            if item['name'] == selected_item:
                current_order_items.pop(i)
                break

        # Update total
        current_order_total = 0.0
        for item in current_order_items:
            current_order_total += item['total']

        # Update displays
        update_order_display()

    def place_order():
        """Place the current order"""
        global current_order_total
        global current_order_items
        global order_counter

        if not current_order_items:
            messagebox.showwarning("Warning", "No items in the order.")
            return

        customer_name = customer_var.get().strip()
        if not customer_name:
            messagebox.showwarning("Warning", "Please enter customer name.")
            return

        # Check inventory and update
        for item in current_order_items:
            item_name = item['name']
            if item_name in inventory:
                if inventory[item_name] < item['quantity']:
                    messagebox.showwarning("Warning",
                                           f"Not enough stock for {item_name}. Only {inventory[item_name]} available.")
                    return
                inventory[item_name] -= item['quantity']
            else:
                messagebox.showwarning("Warning", f"{item_name} not found in inventory.")
                return

        # Save inventory
        if not save_inventory(inventory):
            return

        # Generate order ID
        order_id = f"ORD{order_counter:04d}"
        order_counter += 1

        # Save order
        if save_order(order_id, customer_name, current_order_items, current_order_total, "Completed"):
            # Clear current order
            current_order_items = []
            current_order_total = 0.0

            # Update displays
            update_order_display()
            update_menu_display()

            # Update order counter display
            status_orders_label.config(text=f"Total Orders: {order_counter - 1}")

            # Show success message
            messagebox.showinfo("Success",
                                f"Order placed successfully!\nOrder ID: {order_id}\nTotal: PKR {current_order_total:.2f}")

            # Reset customer name
            customer_var.set("")

    def view_orders():
        """View all orders in a new window"""
        orders = load_orders()

        # Create new window
        orders_window = tk.Toplevel(root)
        orders_window.title("Order History")
        orders_window.geometry("800x500")

        # Create text widget with scrollbar
        orders_text = scrolledtext.ScrolledText(orders_window, width=90, height=25)
        orders_text.pack(padx=10, pady=10)

        if not orders:
            orders_text.insert(tk.END, "No orders found.")
        else:
            for order in orders:
                orders_text.insert(tk.END, f"Order ID: {order['id']}\n")
                orders_text.insert(tk.END, f"Time: {order['timestamp']}\n")
                orders_text.insert(tk.END, f"Customer: {order['customer']}\n")
                orders_text.insert(tk.END, "Items:\n")

                for item in order['items']:
                    orders_text.insert(tk.END,
                                       f"  - {item['name']} x{item['quantity']} @ PKR {item['price']:.2f} = PKR {item['price'] * item['quantity']:.2f}\n")

                orders_text.insert(tk.END, f"Total: PKR {order['total']:.2f}\n")
                orders_text.insert(tk.END, f"Status: {order['status']}\n")
                orders_text.insert(tk.END, "-" * 50 + "\n\n")

        orders_text.configure(state='disabled')

    def add_menu_item():
        """Add a new item to the menu"""
        # Create new window
        add_window = tk.Toplevel(root)
        add_window.title("Add New Menu Item")
        add_window.geometry("400x200")

        # Labels and entries
        tk.Label(add_window, text="Item Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        name_var = tk.StringVar()
        tk.Entry(add_window, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Price (PKR):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        price_var = tk.StringVar()
        tk.Entry(add_window, textvariable=price_var, width=30).grid(row=1, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Initial Stock:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        stock_var = tk.StringVar(value="50")
        tk.Entry(add_window, textvariable=stock_var, width=30).grid(row=2, column=1, padx=10, pady=10)

        def save_new_item():
            name = name_var.get().strip()
            price = price_var.get().strip()
            stock = stock_var.get().strip()

            if not name or not price or not stock:
                messagebox.showwarning("Warning", "Please fill all fields.")
                return

            try:
                price_float = float(price)
                stock_int = int(stock)

                if price_float <= 0:
                    messagebox.showwarning("Warning", "Price must be greater than 0.")
                    return

                if stock_int < 0:
                    messagebox.showwarning("Warning", "Stock cannot be negative.")
                    return
            except:
                messagebox.showwarning("Warning", "Please enter valid numbers for price and stock.")
                return

            # Add to menu
            menu_items[name] = price_float

            # Add to inventory
            inventory[name] = stock_int

            # Save to files
            try:
                # Save to menu file
                with open(MENU_FILE, "a") as file:
                    file.write(f"{name},{price_float}\n")

                # Save to inventory file
                with open(INVENTORY_FILE, "a") as file:
                    file.write(f"{name},{stock_int}\n")

                # Update displays
                update_menu_display()

                # Update item dropdown
                item_menu['menu'].delete(0, 'end')
                for item in menu_items:
                    item_menu['menu'].add_command(label=item, command=tk._setit(item_var, item))

                # Set the new item as selected
                item_var.set(name)

                # Close window
                add_window.destroy()
                messagebox.showinfo("Success", f"{name} added to menu.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to save item: {e}")

        # Buttons
        tk.Button(add_window, text="Save", command=save_new_item, bg="#4CAF50", fg="white", width=15).grid(row=3,
                                                                                                           column=0,
                                                                                                           padx=10,
                                                                                                           pady=20)
        tk.Button(add_window, text="Cancel", command=add_window.destroy, bg="#f44336", fg="white", width=15).grid(row=3,
                                                                                                                  column=1,
                                                                                                                  padx=10,
                                                                                                                  pady=20)

    def reset_order():
        """Reset the current order"""
        global current_order_items
        global current_order_total

        if not current_order_items:
            messagebox.showinfo("Info", "Order is already empty.")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to clear the current order?"):
            current_order_items = []
            current_order_total = 0.0
            update_order_display()
            customer_var.set("")
            messagebox.showinfo("Success", "Order cleared.")

    def view_inventory():
        """View current inventory in a new window"""
        inventory = load_inventory()

        # Create new window
        inv_window = tk.Toplevel(root)
        inv_window.title("Current Inventory")
        inv_window.geometry("400x500")

        # Create text widget with scrollbar
        inv_text = scrolledtext.ScrolledText(inv_window, width=45, height=25)
        inv_text.pack(padx=10, pady=10)

        inv_text.insert(tk.END, "CURRENT INVENTORY\n")
        inv_text.insert(tk.END, "=" * 40 + "\n\n")

        for item, quantity in inventory.items():
            inv_text.insert(tk.END, f"{item:20} : {quantity:4} units\n")

        inv_text.insert(tk.END, "\n" + "=" * 40 + "\n")
        inv_text.insert(tk.END, f"Total Items: {len(inventory)}\n")

        inv_text.config(state='disabled')

        tk.Button(inv_window, text="Close", command=inv_window.destroy,
                  bg="#f44336", fg="white", width=15).pack(pady=10)

    # GUI Layout

    # Title
    title_frame = tk.Frame(root, bg="#4CAF50")
    title_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(title_frame, text="Simple Cafe Management System", font=("Arial", 24, "bold"),
             bg="#4CAF50", fg="white").pack(pady=15)

    # Main content frame
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Left frame - Menu
    left_frame = tk.Frame(main_frame, bg="white", relief="groove", borderwidth=2)
    left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    tk.Label(left_frame, text="Menu", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    # Menu display
    menu_text = tk.Text(left_frame, width=30, height=15, font=("Courier", 10))
    menu_text.pack(padx=10, pady=5)

    # Update menu display
    update_menu_display()

    # Right frame - Order
    right_frame = tk.Frame(main_frame, bg="white", relief="groove", borderwidth=2)
    right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    tk.Label(right_frame, text="Current Order", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

    # Order display
    order_text = tk.Text(right_frame, width=35, height=15, font=("Courier", 10))
    order_text.pack(padx=10, pady=5)

    # Update order display
    update_order_display()

    # Bottom frame - Controls
    bottom_frame = tk.Frame(main_frame, bg="#f0f0f0")
    bottom_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

    # Order controls
    control_frame = tk.Frame(bottom_frame, bg="#f0f0f0")
    control_frame.pack(pady=5)

    tk.Label(control_frame, text="Item:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)

    item_var = tk.StringVar()
    item_menu = ttk.OptionMenu(control_frame, item_var, "", *menu_items.keys())
    item_menu.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(control_frame, text="Quantity:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)

    quantity_var = tk.StringVar(value="1")
    tk.Entry(control_frame, textvariable=quantity_var, width=10).grid(row=0, column=3, padx=5, pady=5)

    tk.Button(control_frame, text="Add to Order", command=add_to_order, bg="#2196F3", fg="white", width=15).grid(row=0,
                                                                                                                 column=4,
                                                                                                                 padx=5,
                                                                                                                 pady=5)
    tk.Button(control_frame, text="Remove from Order", command=remove_from_order, bg="#FF9800", fg="white",
              width=15).grid(row=0, column=5, padx=5, pady=5)

    # Customer info and place order
    customer_frame = tk.Frame(bottom_frame, bg="#f0f0f0")
    customer_frame.pack(pady=5)

    tk.Label(customer_frame, text="Customer Name:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)

    customer_var = tk.StringVar()
    tk.Entry(customer_frame, textvariable=customer_var, width=30).grid(row=0, column=1, padx=5, pady=5)

    tk.Button(customer_frame, text="Place Order", command=place_order, bg="#4CAF50", fg="white", width=15).grid(row=0,
                                                                                                                column=2,
                                                                                                                padx=5,
                                                                                                                pady=5)
    tk.Button(customer_frame, text="Clear Order", command=reset_order, bg="#f44336", fg="white", width=15).grid(row=0,
                                                                                                                column=3,
                                                                                                                padx=5,
                                                                                                                pady=5)
    tk.Button(customer_frame, text="Generate Payment QR", command=generate_qr_code, bg="#9C27B0", fg="white",
              width=20).grid(row=0, column=4, padx=5, pady=5)

    # Menu management buttons
    menu_buttons_frame = tk.Frame(bottom_frame, bg="#f0f0f0")
    menu_buttons_frame.pack(pady=10)

    tk.Button(menu_buttons_frame, text="Add New Menu Item", command=add_menu_item, bg="#9C27B0", fg="white",
              width=20).grid(row=0, column=0, padx=5)
    tk.Button(menu_buttons_frame, text="View Order History", command=view_orders, bg="#607D8B", fg="white",
              width=20).grid(row=0, column=1, padx=5)
    tk.Button(menu_buttons_frame, text="View Inventory", command=view_inventory, bg="#FF9800", fg="white",
              width=20).grid(row=0, column=2, padx=5)
    tk.Button(menu_buttons_frame, text="Refresh Menu", command=update_menu_display, bg="#00BCD4", fg="white",
              width=20).grid(row=0, column=3, padx=5)

    # Configure grid weights
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(0, weight=1)

    # Status bar
    status_frame = tk.Frame(root, bg="#4CAF50", height=30)
    status_frame.pack(fill="x", side="bottom", padx=10, pady=5)

    tk.Label(status_frame, text="Ready", bg="#4CAF50", fg="white").pack(side="left", padx=10)
    status_orders_label = tk.Label(status_frame, text=f"Total Orders: {order_counter - 1}", bg="#4CAF50", fg="white")
    status_orders_label.pack(side="right", padx=10)

    # Set initial menu item if available
    if menu_items:
        first_item = list(menu_items.keys())[0]
        item_var.set(first_item)

    # Start the application
    root.mainloop()


# Run the application
if __name__ == "__main__":
    login()