import tkinter as tk
from tkinter import filedialog
from shutil import copytree, rmtree
import os
import zipfile
import tkinter.messagebox as tkmb

# 定义两个变量来存储目录路径
source_directory = ""
destination_directory = ""

def choose_directory(entry):
    # 打开目录选择对话框
    directory = filedialog.askdirectory()
    if directory:
        # 将选择的目录路径显示在文本框中
        entry.delete(0, tk.END)
        entry.insert(0, directory)
        # 更新全局变量
        global source_directory, destination_directory
        if entry == entry1:
            source_directory = directory
        else:
            destination_directory = directory

def save_and_compress_directories():
    global source_directory, destination_directory
    try:
        # 构建源目录的完整路径
        full_source_path = os.path.join(source_directory, 'resources/app/assets')
        if not os.path.exists(full_source_path):
            raise FileNotFoundError("源目录路径不存在")

        # 在目标路径内新建一个文件夹
        new_folder_name = "new_folder"
        new_folder_path = os.path.join(destination_directory, new_folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        # 将源目录复制到新文件夹中
        copytree(full_source_path, new_folder_path, dirs_exist_ok=True)

        # 压缩文件夹
        zip_filename = os.path.join(destination_directory, new_folder_name + '.sb3')
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(new_folder_path):
                for file in files:
                    # 创建兼容ZIP存档的文件路径
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=destination_directory)
                    zipf.write(file_path, arcname)

        # 删除原始文件夹
        rmtree(new_folder_path)

        tkmb.showinfo("保存成功", )
    except Exception as e:
        # 打印异常的类型和消息
        print(f"Exception: {type(e).__name__}, Message: {e}")
        tkmb.showerror("错误", f"处理目录时出错: {e}")

# 创建主窗口
root = tk.Tk()
root.title("exe转sb3")

# 创建两个文本框用于显示目录路径
label1 = tk.Label(root, text="打包好的程序目录：")
label1.pack()

entry1 = tk.Entry(root, width=50)
entry1.pack()

button1 = tk.Button(root, text="选择", command=lambda: choose_directory(entry1))
button1.pack()

label2 = tk.Label(root, text="保存目录：")
label2.pack()

entry2 = tk.Entry(root, width=50)
entry2.pack()

button2 = tk.Button(root, text="选择", command=lambda: choose_directory(entry2))
button2.pack()

# 添加一个按钮来保存和压缩目录
button_save = tk.Button(root, text="保存", command=save_and_compress_directories, font=("Arial", 16), width=20, height=2)
button_save.pack(pady=20)  # 使用pady增加按钮周围的垂直空间

# 运行主循环
root.mainloop()
