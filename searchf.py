from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  # استخدام PIL لعرض الصورة

import sqlite3
import sys
import os

# تحديد المسار للملفات المضمنة بناءً على البيئة (التطبيق كملف تنفيذي أو أثناء التطوير)
if getattr(sys, 'frozen', False):  # إذا كان التطبيق يعمل كملف تنفيذي
    base_path = sys._MEIPASS  # المسار المؤقت للمحتويات المضمنة
else:
    base_path = os.path.dirname(os.path.abspath(__file__))  # مسار الملف في بيئة التطوير

# الوصول إلى الملفات المضمنة
logo_path = os.path.join(base_path, 'images', 'logo.png')
icon_path = os.path.join(base_path, 'images', 'search.ico')



# دالة لإغلاق الاتصال بقاعدة البيانات
def close_db_connection():
    if db:
        db.close()

# الاتصال بقاعدة البيانات بشكل آمن
try:
    db = sqlite3.connect("./data.db")
except sqlite3.Error as e:

    messagebox.showerror("Database Error", f"Error connecting to database: {e}")
    db = None

# تحديد أسماء الشركات المدرجة
COMPANY_query = db.execute("SELECT COMPANY FROM lens_price GROUP BY COMPANY")

# أنشاء النافذه الأساسية 
root = Tk()
root.title("Search") # عنوان النافذة
root.minsize(500, 500)
root.iconbitmap("./search.ico") # الشعار
root["background"] = "#99bfbf" # خلفية البرنامج
# إضافة أيقونة للنافذة

# تحميل صورة الشعار باستخدام PIL
logo_image = Image.open("./logo.png")  # استبدل بالمسار الفعلي للشعار
logo_image = logo_image.resize((60, 60))  # تغيير حجم الصورة إذا لزم الأمر
logo_photo = ImageTk.PhotoImage(logo_image)

# إضافة الشعار إلى نافذة التطبيق باستخدام Label
logo_label = Label(root, image=logo_photo, bg="#0D1B4C")  # تعيين الخلفية لتتناسب مع البرنامج
logo_label.grid(row=0, column=0, padx=10, pady=10)

# قائمة أسماء الشركات
company_list = ["Select Company Name"]
for row in COMPANY_query:
    company_list.append(row[0])

# دالة لاختيار أسماء العلامات التجارية بناءً على الشركة المختارة
def select_brands(e):
    brand_name = ["Select Brand Name"]
    statement = """SELECT BRAND FROM lens_price WHERE COMPANY=:COMPANY GROUP BY BRAND"""
    brand_query = db.execute(statement, {"COMPANY": company_name.get()})

    for t in brand_query:
        brand_name.append(t[0])  # إضافة أول عمود (brand_name) من كل صف

    brand_list.config(values=brand_name)  # تحديث قائمة البراندات
    brand_list.current(0)  # ضبط القيمة الافتراضية 
def search():
    # التحقق من صحة المدخلات
    search_value = search_box.get()
    brand_choice = brand_list.get()
    company_choice = company_name.get()

    # إذا لم يتم اختيار شركة، نعرض جميع البيانات
    if company_choice == "Select Company Name":
        company_choice = None  # تعيين الشركة إلى None ليتم تجاهلها في الاستعلام
 
    # بناء المعاملات لاستعلام البحث
    params = []  # قائمة المعاملات ستكون فارغة في البداية

    query = "SELECT * FROM lens_price"  # الاستعلام الأساسي

    # إضافة شرط الشركة إذا تم تحديدها
    if company_choice:
        query += " WHERE Company=?"
        params.append(company_choice)

        # إذا تم اختيار العلامة التجارية، نضيفها إلى الاستعلام
        if brand_choice != "Select Brand Name":
            query += " AND Brand=?"
            params.append(brand_choice)
    # else:
    #     # إذا لم يتم اختيار الشركة، نضيف شرط العلامة التجارية فقط إذا تم تحديدها
    #     if brand_choice != "Select Brand Name":
    #         query += " WHERE Brand=?"
    #         params.append(brand_choice)

    # إذا كان search_value غير فارغ، نضيفه إلى المعاملات ونعدل الاستعلام
    if search_value:
        if selected_column_var.get() == "Lens Index":
            selected_column = "Lens_Index"
        else:
            selected_column = selected_column_var.get()

        # إضافة شرط البحث في العمود المحدد
        if params:
            query += f" AND {selected_column} LIKE ?"
        else:
            query += f" WHERE {selected_column} LIKE ?"
        
        params.append(f"%{search_value}%")  # إضافة search_value إلى المعاملات
    
    try:

        search_results = db.execute(query, tuple(params))
    except sqlite3.Error as e:
        messagebox.showerror("SQL Error", f"Error executing query: {e}")
        return

    # حذف الصفوف القديمة في الجدول قبل عرض النتائج الجديدة
    for item in Errortree.get_children():
        Errortree.delete(item)

    # إدراج النتائج في الجدول
    for row in search_results:
        Errortree.insert("", "end", values=row)


# دالة لفرز البيانات
def sort_column(col, reverse):
    data = [(Errortree.item(child)["values"], child) for child in Errortree.get_children()]
    
    # التحقق من تحويل القيم إلى نصوص للفرز
    data.sort(key=lambda x: str(x[0][col]) if x[0][col] is not None else "", reverse=reverse)

    # إعادة ترتيب الصفوف في Treeview بناءً على البيانات المرتبة
    for index, (values, child) in enumerate(data):
        Errortree.move(child, '', index)

    sort_columns[col] = not reverse  # تغيير ترتيب التصفية (Ascending/Descending)

# دالة لتعديل عرض الأعمدة بناءً على أطول قيمة في العمود
def auto_adjust_columns(treeview, data):
    for col in treeview["columns"]:
        max_width = len(col)  # بدءًا من طول اسم العمود
        for row in data:
            value = row[treeview["columns"].index(col)]
            max_width = max(max_width, len(str(value)))  # تحديد أطول نص في العمود
        treeview.column(col, width=max_width * 7)  # تعيين العرض بناءً على أطول قيمة

# قائمة الأعمدة للاختيار
columns = ["Lens Index", "Coating", "Type", "Price"]
selected_column_var = StringVar(value="Lens Index")  # العمود الافتراضي

# إنشاء إطار للأزرار الراديو
radio_frame = Frame(root, bg="#1D1B4C")
radio_frame.grid(row=0, column=0, columnspan=4, pady=25)

# إضافة الأزرار الراديو
for column in columns:
    Radiobutton(radio_frame, text=column, variable=selected_column_var, value=column,
                highlightthickness=3, selectcolor="navy", foreground="white",
                font=("Arial", 16, "bold"), background="#1F6699",
                padx=4, pady=4).pack(side=LEFT)

# حقل البحث
search_box = Entry(root, width=20, fg="blue", font=("Arial", 16, "bold"))
search_box.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# إنشاء قائمة منسدلة لاختيار الشركة
company_name = ttk.Combobox(root, value=company_list, width=20, font=("Arial", 12))
company_name.current(0)
company_name.bind("<<ComboboxSelected>>", select_brands)
company_name.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# إنشاء قائمة منسدلة لاختيار العلامة التجارية
brand_list = ttk.Combobox(root, value=[" "], width=20, font=("Arial", 12))
brand_list.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

# زر البحث
search_button = Button(root, text="Search", padx=2, pady=2, width=20,
                       highlightthickness=5, font=("Arial", 10, "bold"),
                       bg="#1F6699", fg="white", command=search)

search_button.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

# إعداد الجدول
cursor = db.execute("SELECT * FROM lens_price")
# table_headers = list(map(lambda x: x[0], cursor.description))
table_headers = [col[0].replace('_', ' ') for col in cursor.description]
sort_columns = [False] * len(table_headers)

# إعداد الجدول Treeview
Errortree = ttk.Treeview(root, columns=table_headers, show="headings", height=10)


# تخصيص الأعمدة
for i, header in enumerate(table_headers):
    Errortree.heading(f"#{i+1}", text=header, command=lambda _col=i: sort_column(_col, sort_columns[_col]))
    Errortree.column(f"#{i+1}", stretch=YES)

# تحميل البيانات
rows = cursor.fetchall()
for row in rows:
    Errortree.insert("", "end", values=row)

# تعديل عرض الأعمدة بناءً على البيانات
auto_adjust_columns(Errortree, rows)

# وضع الجدول في واجهة المستخدم
Errortree.grid(row=2, column=0, columnspan=4, sticky="nsew")

# إضافة Scrollbars
vsb = ttk.Scrollbar(root, orient="vertical", command=Errortree.yview)
vsb.grid(row=2, column=4, sticky='ns')
Errortree.configure(yscrollcommand=vsb.set)

hsb = ttk.Scrollbar(root, orient="horizontal", command=Errortree.xview)
hsb.grid(row=3, column=0, columnspan=4, sticky='ew')
Errortree.configure(xscrollcommand=hsb.set)

# ضبط تخطيط الأعمدة
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

# إضافة footer في الأسفل
footer = Label(root, text="Version 1.0 | Developed by Elhussein Taha", fg="white", bg="#0D1B40", font=("Arial", 10))
footer.grid(row=4, column=0, columnspan=4, pady=10)

root.mainloop()


# to build your app use 
""" python -m PyInstaller ./search1.py --onefile --windowed --add-data "./logo.png;images" --add-data "./search.ico;images" --icon=./search.ico"""
