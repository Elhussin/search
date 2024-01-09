from tkinter import *
from collections import OrderedDict
from tkinter import filedialog, ttk
import sqlite3

db = sqlite3.connect("./data.db")
# s=ttk.Style()
COMPANY_query = db.execute("SELECT COMPANY FROM lens_price GROUP By COMPANY")


root = Tk()

root.title("Searh")
root.minsize(500, 500)
root.iconbitmap("./search.ico")
root["background"] = "#0D1B4C"
#  company name list
comapny = ["Select Company Name"]
for row in COMPANY_query:
    comapny.append(row)


# functian to selct bran name for the company
def select_brands(e):
    brand_name = ["Select Brand Name"]
    statement = (
        """SELECT BRAND FROM lens_price WHERE  COMPANY=:COMPANY  GROUP By BRAND"""
    )
    brand_query = db.execute(statement, {"COMPANY": company_name.get()})
    brand_name

    for t in brand_query:
        for x in t:
            brand_name.append(x)

    brand_list.config(value=brand_name)
    brand_list.current(0)


def search():
    for item in Errortree.get_children():
        Errortree.delete(item)
    search_DATE = 0
    search_value = search_box.get()

    brand_choice = brand_list.get()
    company_choice = company_name.get()
    select_coulman = selected_columan.get()

    search_DATE
    if select_coulman == "Lens Index":
        if brand_choice == "Select Brand Name":
            stat = "SELECT * FROM lens_price WHERE  Lens_Index  LIKE ?  and  Company=? "
            search_DATE = db.execute(
                stat,
                (
                    f"%{search_value}%",
                    company_choice,
                ),
            )
        else:
            stat = "SELECT * FROM lens_price WHERE  Lens_Index  LIKE ?  and  Company=?  and Brand =?  "
            search_DATE = db.execute(
                stat, (f"%{search_value}%", company_choice, brand_choice)
            )
    if select_coulman == "Coating":
        if brand_choice == "Select Brand Name":
            stat = "SELECT * FROM lens_price WHERE  Coating  LIKE ?  and  Company=? "
            search_DATE = db.execute(
                stat,
                (
                    f"%{search_value}%",
                    company_choice,
                ),
            )
        else:
            stat = "SELECT * FROM lens_price WHERE  Coating  LIKE ?  and  Company=?  and Brand =?  "
            search_DATE = db.execute(
                stat, (f"%{search_value}%", company_choice, brand_choice)
            )
    if select_coulman == "Type":
        if brand_choice == "Select Brand Name":
            stat = "SELECT * FROM lens_price WHERE  Type  LIKE ?  and  Company=? "
            search_DATE = db.execute(
                stat,
                (
                    f"%{search_value}%",
                    company_choice,
                ),
            )
        else:
            stat = "SELECT * FROM lens_price WHERE  Type  LIKE ?  and  Company=?  and Brand =?  "
            search_DATE = db.execute(
                stat, (f"%{search_value}%", company_choice, brand_choice)
            )
    if select_coulman == "Price":
        if brand_choice == "Select Brand Name":
            stat = "SELECT * FROM lens_price WHERE  Price  LIKE ?  and  Company=? "
            search_DATE = db.execute(
                stat,
                (
                    f"%{search_value}%",
                    company_choice,
                ),
            )
        else:
            stat = "SELECT * FROM lens_price WHERE  Price  LIKE ?  and  Company=?  and Brand =?  "
            search_DATE = db.execute(
                stat, (f"%{search_value}%", company_choice, brand_choice)
            )

    for i in search_DATE:
        Errortree.insert("", "end", values=i)


#  select coulman to search on it
lst = ["Lens Index", "Coating", "Type", "Price"]
#  creat radio butoon to hoise the coulman
selected_columan = StringVar()

for i in range(len(lst)):
    select_search_coulman = Radiobutton(
        text=lst[i],
        variable=selected_columan,
        value=lst[i],
        highlightthickness=3,
        selectcolor="navy",
        foreground="white",
        font=("Arial", 16, "bold"),
        background="#3F6699",
        padx=2,
        pady=2,
        width=20,
    )
    select_search_coulman.grid(column=i + 1, row=0, sticky="W")
selected_columan.set("Lens Index")


search_box = Entry(root, width=20, fg="blue", font=("Arial", 16, "bold"), borderwidth=1)
search_box.grid(row=1, column=1, padx=10, pady=10)


#  creat rb box for company
company_name = ttk.Combobox(root, value=comapny, width=20, font=("Arial", 12), height=6)
company_name.current(0)
# bind the combobox
company_name.bind("<<ComboboxSelected>>", select_brands)

company_name.grid(row=1, column=2, padx=10, pady=10)

brand_list = ttk.Combobox(
    root,
    value=[" "],
    width=20,
    font=(
        "Arial",
        12,
    ),
    height=6,
)
brand_list.grid(row=1, column=3, padx=10, pady=10)
search_but = Button(
    root,
    text="search",
    padx=2,
    pady=2,
    width=20,
    highlightthickness=5,
    font=("Arial", 10, "bold"),
    bg="#3F6699",
    command=search,
)
search_but.grid(row=1, column=4)


style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview.Heading", background="black", foreground="RED")
#  tree view
teable_header = ()
cursor = db.execute("select * from lens_price")
teable_header = list(map(lambda x: x[0], cursor.description))
for i in range(len(teable_header)):
    if teable_header[i] == "Lens_Index":
        teable_header[i] = "Index"

# creat tree view
Errortree = ttk.Treeview(root, columns=teable_header, show="headings", height=30)
count = 1
for i in teable_header:
    Errortree.heading("#" + str(count), text=i, anchor="w")
    Errortree.column("#" + str(count), stretch=YES)

    # anchor=CENTER, stretch=NO, width=100
    count += 1
for i in cursor:
    Errortree.insert("", "end", values=i)
Errortree.grid(row=2, column=0, columnspan=15, rowspan=2)
style = ttk.Style(root)
style.theme_use("clam")
style.configure(
    "Treeview.Heading",
    background="#494646",
    foreground="RED",
    font=("Arial", 12, "bold"),
)
style.configure(
    "Treeview",
    background="#cedded",
    foreground="black",
    fieldbackground="cedded",
    font=("Arial", 11),
)

# foreground="white"
root.mainloop()
