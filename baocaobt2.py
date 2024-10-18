import psycopg2
from psycopg2 import sql
import tkinter as tk
from tkinter import messagebox, ttk


# Hàm kết nối đến cơ sở dữ liệu
def connect_to_db(username, password):
    try:
        connection = psycopg2.connect(
            dbname="MyDatabase",  
            user=username,
            password=password,
            host="localhost"
        )
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
        return connection
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể kết nối đến cơ sở dữ liệu: {e}")
        return None


# Chức năng tìm kiếm sản phẩm không phân biệt hoa thường
def search_product(connection, product_name):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM products WHERE product_name ILIKE %s"
        cursor.execute(query, ('%' + product_name + '%',))  
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tìm sản phẩm: {e}")
        return None


# Chức năng thêm sản phẩm mới
def add_product(connection, product_name, product_price, category_id):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO products (product_name, product_price, category_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (product_name, product_price, category_id))
        connection.commit()
        cursor.close()
        messagebox.showinfo("Thành công", "Thêm sản phẩm thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm sản phẩm: {e}")


# Giao diện đăng nhập
def login_form():
    window = tk.Tk()
    window.title("Đăng Nhập Hệ Thống")
    window.geometry("400x250")  
    window.configure(bg="#F0F0F0")
    
    tk.Label(window, text="Đăng Nhập", font=("Helvetica", 20, "bold"), bg="#F0F0F0", fg="#4CAF50").pack(pady=15)

    login_frame = ttk.Frame(window)
    login_frame.pack(pady=10)

    tk.Label(login_frame, text="Tên đăng nhập:", bg="#F0F0F0", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    username_entry = ttk.Entry(login_frame, width=30)
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_frame, text="Mật khẩu:", bg="#F0F0F0", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    password_entry = ttk.Entry(login_frame, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)
    
    def login_action():
        username = username_entry.get()
        password = password_entry.get()
        connection = connect_to_db(username, password)
        if connection:
            window.destroy()  
            show_menu(connection)
    window.bind('<Return>', lambda event: login_action())

    ttk.Button(window, text="Đăng Nhập", command=login_action, style='TButton').pack(pady=15)

    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=6)  
    window.mainloop()

# Menu chính sau khi đăng nhập
def show_menu(connection):
    menu_window = tk.Tk()
    menu_window.title("Menu Quản Lý Sản Phẩm")
    menu_window.geometry("500x400")
    menu_window.configure(bg="#EAF6F6")

    tk.Label(menu_window, text="Quản Lý Sản Phẩm", font=("Helvetica", 24, "bold"), bg="#EAF6F6", fg="#056676").pack(pady=30)
    ttk.Button(menu_window, text="Đăng Xuất", command=lambda: (menu_window.destroy(), login_form()), style='TButton').place(relx=0, rely=1, anchor='sw')

    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12, ), padding=12)  
    style.configure('TFrame', background="#EAF6F6")
    
    # Chức năng tìm kiếm sản phẩm
    def search_product_form():
        search_window = tk.Toplevel(menu_window)
        search_window.title("Tìm Kiếm Sản Phẩm")
        search_window.geometry("550x500")
        search_window.configure(bg="#EAF6F6")

        tk.Label(search_window, text="Tìm Kiếm Sản Phẩm", font=("Helvetica", 18, "bold"), bg="#EAF6F6", fg="#4CAF50").pack(pady=20)
        search_frame = ttk.Frame(search_window)
        search_frame.pack(pady=10)
        tk.Label(search_frame, text="Tên sản phẩm:", font=("Arial", 13), bg="#EAF6F6").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    
        product_name_entry = ttk.Entry(search_frame, width=40, font=("Arial", 12)) 
        product_name_entry.grid(row=0, column=1, padx=5, pady=5)
    
        result_frame = ttk.Frame(search_window)
        result_frame.pack(pady=20)

        def search_action():
            product_name = product_name_entry.get()
            result_listbox.delete(0, tk.END)  
            results = search_product(connection, product_name)
            if results:
                for row in results:
                    result_listbox.insert(tk.END, f"ID: {row[0]}, Tên: {row[1]}, Giá: {row[2]:.2f}, Danh mục: {row[3]}")
            else:
                result_listbox.insert(tk.END, "Không tìm thấy sản phẩm nào.")
 
        search_window.bind('<Return>', lambda event: search_action())

        button_frame = ttk.Frame(search_window)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Trở Lại", command=lambda: (search_window.destroy(), menu_window.deiconify()), style='TButton').pack(side=tk.LEFT, padx=20, pady=10)
        ttk.Button(button_frame, text="Tìm Kiếm", command=search_action, style='TButton').pack(side=tk.LEFT, padx=20, pady=10)

        result_label = tk.Label(result_frame, text="Kết quả tìm kiếm:", bg="#EAF6F6", font=("Arial", 12))
        result_label.pack(anchor=tk.W)

        result_listbox = tk.Listbox(result_frame, width=81, height=10)
        result_listbox.pack(pady=10)
        menu_window.withdraw() 
        product_name_entry.focus()

    # Chức năng thêm sản phẩm
    def add_product_form():
        add_window = tk.Toplevel(menu_window)
        add_window.title("Thêm Sản Phẩm Mới")
        add_window.geometry("400x300")
        add_window.configure(bg="#EAF6F6")

        tk.Label(add_window, text="Tên sản phẩm:", font=("Arial", 12), bg="#EAF6F6").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        product_name_entry = ttk.Entry(add_window, width=30)
        product_name_entry.grid(row=0, column=1, padx=10, pady=14)

        tk.Label(add_window, text="Giá sản phẩm:", font=("Arial", 12), bg="#EAF6F6").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        product_price_entry = ttk.Entry(add_window, width=30)
        product_price_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(add_window, text="Mã danh mục:", font=("Arial", 12), bg="#EAF6F6").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        category_id_entry = ttk.Entry(add_window, width=30)
        category_id_entry.grid(row=2, column=1, padx=10, pady=10)

        def add_action():
            product_name = product_name_entry.get()
            product_price = product_price_entry.get()
            category_id = category_id_entry.get()
            add_product(connection, product_name, product_price, category_id)

        menu_window.withdraw()     
        product_name_entry.focus()

        add_window.bind('<Return>', lambda event: add_action())

        button_frame = ttk.Frame(add_window)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Trở Lại", command=lambda: (add_window.destroy(), menu_window.deiconify()), style='TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Thêm Sản Phẩm", command=add_action, style='TButton').pack(side=tk.LEFT, padx=10)

    ttk.Button(menu_window, text="Tìm Kiếm Sản Phẩm", command=search_product_form, style='TButton').pack(pady=20)
    ttk.Button(menu_window, text="Thêm Sản Phẩm Mới", command=add_product_form, style='TButton').pack(pady=20)

    menu_window.mainloop()

login_form()
