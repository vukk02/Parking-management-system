import os

# Đường dẫn đến thư mục chứa tệp .txt
folder_path = r'D:\Desktop\New folder (2)\img'

# Lấy danh sách các tệp trong thư mục
files = os.listdir(folder_path)

# Lọc chỉ các tệp là .txt
txt_files = [file for file in files if file.endswith('.txt')]

# Sắp xếp danh sách để đổi tên theo thứ tự
txt_files.sort()

# Đổi tên từng tệp
for index, file in enumerate(txt_files, start=1):
    # Tạo tên mới
    new_name = f"{index}.jpg"
    
    # Đường dẫn cũ và mới
    old_path = os.path.join(folder_path, file)
    new_path = os.path.join(folder_path, new_name)
    
    # Đổi tên
    os.rename(old_path, new_path)

print("Đã đổi tên các file .txt xong!")




















