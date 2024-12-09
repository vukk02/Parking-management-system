import threading
import tkinter as tk
from tkinter import ttk
from flask import Flask, render_template, request, redirect
import mysql.connector

# Flask app setup
app = Flask(__name__)

# Kết nối cơ sở dữ liệu MySQL
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='12342345',
        database='booking_system'
    )

# Route trang chính
@app.route('/')
def index():
    return render_template('index.html')

# Xử lý form gửi dữ liệu
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    phone = request.form['phone']
    reservation_time = request.form['reservation_time']
    license_plate = request.form['license_plate']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO reservations (name, phone, reservation_time, license_plate) VALUES (%s, %s, %s, %s)',
        (name, phone, reservation_time, license_plate)
    )
    conn.commit()
    conn.close()

    return redirect('/')

# Hàm lấy dữ liệu từ MySQL
def get_reservations():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reservations')
    reservations = cursor.fetchall()
    conn.close()
    return reservations

# Tkinter app
def tkinter_app():
    def update_treeview():
        # Xóa dữ liệu cũ
        for item in tree.get_children():
            tree.delete(item)

        # Lấy dữ liệu từ MySQL
        reservations = get_reservations()
        for reservation in reservations:
            tree.insert("", tk.END, values=reservation)

        # Lên lịch tự động làm mới sau 5 giây
        root.after(5000, update_treeview)

    # Giao diện Tkinter
    root = tk.Tk()
    root.title("Thông tin đặt chỗ")

    tree = ttk.Treeview(root, columns=("ID", "Tên", "SĐT", "Thời gian", "Biển số"), show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    tree.heading("ID", text="ID")
    tree.heading("Tên", text="Tên")
    tree.heading("SĐT", text="SĐT")
    tree.heading("Thời gian", text="Thời gian")
    tree.heading("Biển số", text="Biển số")

    # Cập nhật dữ liệu ban đầu và tự động làm mới
    update_treeview()

    root.mainloop()
# Chạy Flask trong một thread
def run_flask():
    app.run(debug=True, use_reloader=False)

# Main
if __name__ == "__main__":
    # Chạy Flask trên luồng riêng
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Chạy Tkinter
    tkinter_app()