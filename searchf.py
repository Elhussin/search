from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # To display images using PIL (Pillow)
import sqlite3
import sys
import os
from pystray import Icon, MenuItem, Menu
import pystray

# Check if the script is running as a frozen executable (PyInstaller)
if getattr(sys, 'frozen', False):
    # Path used during running the executable created by PyInstaller
    application_path = sys._MEIPASS
else:
    # Path used during development
    application_path = os.path.dirname(os.path.abspath(__file__))

# Paths to access the necessary files
data_db_path = os.path.join(application_path, 'data.db')
logo_path = os.path.join(application_path, 'assets/logo.png')
icon_path = os.path.join(application_path, 'assets/search.ico')

# Try to connect to the SQLite database, display error message if connection fails
try:
    db = sqlite3.connect(data_db_path)  # Path to database
except sqlite3.Error as e:
    # Display error message if connection fails
    messagebox.showerror("Database Error", f"Error connecting to database: {e}")
    db = None

# Query to get unique company names from the database
COMPANY_query = db.execute("SELECT COMPANY FROM lens_price GROUP BY COMPANY") if db else []

# Main application window (Tkinter root window)
root = Tk()
root.title("Search")  # Window title
root.minsize(800, 700)  # Minimum size
root["background"] = "#99bfbf"  # Background color
root.iconbitmap(icon_path)  # Application icon

# Try to load and display the logo image
try:
    logo_image = Image.open(logo_path)
    logo_image = logo_image.resize((60, 60))  # Resize image (optional)
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Add logo to the application window
    logo_label = Label(root, image=logo_photo, bg="#99bfbf")
    logo_label.grid(row=0, column=0, padx=10, pady=10)
except FileNotFoundError:
    messagebox.showerror("File Not Found", "Logo image file not found.")

# List of companies for the dropdown menu
company_list = ["Select Company Name"]
for row in COMPANY_query:
    company_list.append(row[0])

# Function to fetch and populate brands based on selected company
def select_brands(e):
    brand_name = ["Select Brand Name"]
    if db:
        statement = "SELECT BRAND FROM lens_price WHERE COMPANY=:COMPANY GROUP BY BRAND"
        brand_query = db.execute(statement, {"COMPANY": company_name.get()})
        for t in brand_query:
            brand_name.append(t[0])

    brand_list.config(values=brand_name)  # Update dropdown options
    brand_list.current(0)  # Set default value

# Function to handle search queries
def search():
    # Validate user inputs
    search_value = search_box.get()
    brand_choice = brand_list.get()
    company_choice = company_name.get()

    # If no company is selected, show all data
    if company_choice == "Select Company Name":
        company_choice = None  # Set company to None to ignore it in the query
 
    # Initialize parameters for the search query
    params = []  # Empty list of parameters to start

    query = "SELECT * FROM lens_price"  # Base query

    # Add company condition if selected
    if company_choice:
        query += " WHERE Company=?"
        params.append(company_choice)

        # If a brand is selected, add it to the query
        if brand_choice != "Select Brand Name":
            query += " AND Brand=?"
            params.append(brand_choice)

    # If search value is provided, add it to the query
    if search_value:
        if selected_column_var.get() == "Lens Index":
            selected_column = "Lens_Index"
        else:
            selected_column = selected_column_var.get()

        # Add search condition for the selected column
        if params:
            query += f" AND {selected_column} LIKE ?"
        else:
            query += f" WHERE {selected_column} LIKE ?"
        
        params.append(f"%{search_value}%")  # Append search value to parameters
    
    try:
        # Execute the search query
        search_results = db.execute(query, tuple(params))
    except sqlite3.Error as e:
        messagebox.showerror("SQL Error", f"Error executing query: {e}")
        return

    # Delete old rows in the table before inserting new results
    for item in Errortree.get_children():
        Errortree.delete(item)

    # Insert search results into the table
    for row in search_results:
        Errortree.insert("", "end", values=row)


# Function to sort columns in the Treeview
def sort_column(col, reverse):
    # Extract the data from the table
    data = [(Errortree.item(child)["values"], child) for child in Errortree.get_children()]

    def safe_key(x):
        value = x[0][col]  # Target value for sorting
        if value is None or value == '':
            return (1, '')  # Empty values should appear at the end
        try:
            # Try converting the value to a number
            return (0, float(value))  # Numbers are prioritized
        except ValueError:
            # If not a number, return the value as a string
            return (1, str(value).lower())  # Strings are given lower priority

    # Sort the data using the safe key
    data.sort(key=lambda x: safe_key(x), reverse=reverse)

    # Rearrange the rows in the Treeview based on the sorted data
    for index, (values, child) in enumerate(data):
        Errortree.move(child, '', index)

    # Update the sorting state
    sort_columns[col] = not reverse


# Adjust column width based on content
def auto_adjust_columns(treeview, data):
    for col in treeview["columns"]:
        max_width = len(col)
        for row in data:
            value = row[treeview["columns"].index(col)]
            max_width = max(max_width, len(str(value)))
        treeview.column(col, width=max_width * 7)


# Search filters
columns = ["Lens Index", "Coating", "Type", "Price"]
selected_column_var = StringVar(value="Lens Index")

radio_frame = Frame(root, bg="#99bfbf")
radio_frame.grid(row=0, column=1, columnspan=3)

# Create radio buttons for selecting search column
for column in columns:
    Radiobutton(radio_frame, text=column, variable=selected_column_var, value=column,
                highlightthickness=3, selectcolor="navy", foreground="white",
                font=("Arial", 16, "bold"), background="#1F6699",
                padx=4, pady=4).pack(side=LEFT)


# Search box
search_box = Entry(root, width=20, fg="blue", font=("Arial", 16, "bold"))
search_box.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Dropdown for companies
company_name = ttk.Combobox(root, value=company_list, width=20, font=("Arial", 12))
company_name.current(0)
company_name.bind("<<ComboboxSelected>>", select_brands)
company_name.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Dropdown for brands
brand_list = ttk.Combobox(root, value=[" "], width=20, font=("Arial", 12))
brand_list.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

# Search button
search_button = Button(root, text="Search", padx=2, pady=2, width=20,
                       highlightthickness=5, font=("Arial", 10, "bold"),
                       bg="#1F6699", fg="white", command=search)

search_button.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

# Treeview for displaying results
cursor = db.execute("SELECT * FROM lens_price")
table_headers = [col[0].replace('_', ' ') for col in cursor.description]
sort_columns = [False] * len(table_headers)
Errortree = ttk.Treeview(root, columns=table_headers, show="headings", height=10)
for i, header in enumerate(table_headers):
    Errortree.heading(f"#{i+1}", text=header, command=lambda _col=i: sort_column(_col, sort_columns[_col]))
    Errortree.column(f"#{i+1}", stretch=YES)

# Insert data
rows = cursor.fetchall()
for row in rows:
    Errortree.insert("", "end", values=row)

# Fit column widths with data
auto_adjust_columns(Errortree, rows)

# Add table to layout
Errortree.grid(row=2, column=0, columnspan=4, sticky="nsew")

# Scrollbars
vsb = ttk.Scrollbar(root, orient="vertical", command=Errortree.yview)
vsb.grid(row=2, column=4, sticky='ns')
Errortree.configure(yscrollcommand=vsb.set)

hsb = ttk.Scrollbar(root, orient="horizontal", command=Errortree.xview)
hsb.grid(row=3, column=0, columnspan=4, sticky='ew')
Errortree.configure(xscrollcommand=hsb.set)

# Layout configuration
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# App Footer
footer = Label(root, text="Version 1.1 | Developed by Elhussein Taha", fg="white", bg="#0D1B40", font=("Arial", 10))
footer.grid(row=4, column=0, columnspan=4, pady=10)

root.mainloop()


# # Function to set up the taskbar icon using pystray
# def create_image():
#     # Open the icon image using Pillow
#     image = Image.open(icon_path)
#     return image

# def on_quit(icon, item):
#     icon.stop()

# # Set up the taskbar icon
# def set_taskbar_icon():
#     # Open the icon image using PIL
#     icon_image = create_image()

#     # Set up the icon using pystray
#     icon = Icon("MyApp", icon_image, menu=Menu(MenuItem("Quit", on_quit)))
    
#     # Run the icon in the taskbar
#     icon.run()

# if __name__ == '__main__':
#     set_taskbar_icon()


# Build your app with PyInstaller using:
# python -m PyInstaller ./search.py --onefile --windowed --add-data "./logo.png;assets" --add-data "./search.ico;assets" --icon=./search.ico

# to build your app use 
""" python -m PyInstaller ./search.py --onefile --windowed --add-data "./logo.png;images" --add-data "./search.ico;images" --icon=./search.ico"""
# pyinstaller --onefile --windowed  --add-data "data.db;." --add-data "assets/logo.png;assets" --add-data "assets/search.ico;assets" search.py
