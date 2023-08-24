import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import pyheif
import os
import shutil

def open_file_dialog():
    filetypes = [('HEIC Files', '*.heic')]
    return filedialog.askopenfilenames(title='Select HEIC Files', filetypes=filetypes)

def select_save_directory():
    global save_directory
    save_directory = filedialog.askdirectory(title='Select Save Directory')

def preview_images():
    global image_paths, preview_progress, image_previews
    image_paths = open_file_dialog()
    preview_frame.delete("1.0", tk.END)

    tmp_folder = ".tmp"
    os.makedirs(tmp_folder, exist_ok=True)

    preview_progress['maximum'] = len(image_paths)
    preview_progress['value'] = 0

    image_previews = []
    for index, path in enumerate(image_paths):
        heif_file = pyheif.read(path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        filename = os.path.basename(path)
        jpg_path = os.path.join(tmp_folder, filename.replace('.heic', '.jpg'))

        image.thumbnail((200, 200))  # 调整图片大小以适应预览窗口
        image.save(jpg_path, format='JPEG', quality=10)  # 转换为低质量的JPG图片

        img = Image.open(jpg_path)  # 重新打开转换后的JPG图片
        img_tk = ImageTk.PhotoImage(img)
        image_previews.append(img_tk)  # 保存对图像对象的引用

        preview_frame.image_create(tk.END, image=img_tk)
        preview_frame.insert(tk.END, '\n')

        preview_progress['value'] = index + 1
        root.update()  # 更新主窗口，以刷新进度条显示

    preview_frame.config(state=tk.NORMAL)  # 恢复预览窗口的状态为可编辑


def convert_images():
    if not save_directory:
        return

    progress_bar['maximum'] = len(image_paths)
    for index, src_path in enumerate(image_paths):
        try:
            heif_file = pyheif.read(src_path)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
            filename = os.path.basename(src_path)
            new_file_path = os.path.join(save_directory, filename.replace('.heic', '.jpg'))
            image.save(new_file_path, format='JPEG')

            progress_bar['value'] = index + 1
            progress_bar.update()

        except Exception as e:
            print(f'转换 {src_path} 出错：{str(e)}')

    progress_bar.stop()
    completed_label.configure(text="转换完成")

def on_closing():
    shutil.rmtree(".tmp")  # 删除.tmp文件夹
    root.destroy()

# 创建主窗口
root = tk.Tk()
root.title('HEIC to JPG Converter')

# 创建上传按钮
upload_button = tk.Button(root, text='Upload HEIC Files', command=preview_images, padx=10, pady=10)
upload_button.pack()

# 创建预览进度条
preview_progress = ttk.Progressbar(root, length=200, mode='determinate')
preview_progress.pack()

# 创建预览窗口
preview_frame = tk.Text(root, height=10, width=50)
preview_frame.pack()
preview_frame.config(state=tk.DISABLED)  # 初始化预览窗口为不可编辑状态

# 创建选择保存路径按钮
save_directory_button = tk.Button(root, text='Select Save Directory', command=select_save_directory, padx=10, pady=10)
save_directory_button.pack()

# 创建转换按钮
convert_button = tk.Button(root, text='Convert to JPG', command=convert_images, padx=10, pady=10)
convert_button.pack()

# 创建转换进度条
progress_bar = ttk.Progressbar(root, length=200, mode='determinate')
progress_bar.pack()

# 创建转换完成提示
completed_label = tk.Label(root, text="")
completed_label.pack()

# 保存目录
save_directory = ''

# 替换关闭按钮，并关联关闭窗口事件
close_button = tk.Button(root, text="Close", command=on_closing)
close_button.pack()

# 运行主循环
root.mainloop()
