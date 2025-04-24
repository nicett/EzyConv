import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os
import threading

def convert_webp_to_gif(input_files, output_folder, progress_var, progress_label):
    """
    异步将 WebP 文件转换为 GIF 格式，避免阻塞 UI 线程。

    参数:
    - input_files: 要转换的 WebP 文件路径列表
    - output_folder: 转换后的文件保存路径
    - progress_var: 进度条变量，用于更新转换进度
    - progress_label: 标签变量，用于更新进度百分比文字
    """
    total_files = len(input_files)
    count_success = 0
    count_fail = 0
    count_skip = 0

    for i, file_path in enumerate(input_files):
        if file_path.lower().endswith('.webp'):
            try:
                with Image.open(file_path) as im:
                    base_name = os.path.basename(file_path)
                    output_path = os.path.join(output_folder, os.path.splitext(base_name)[0] + '.gif')
                    im.save(output_path, "gif", save_all=True)
                    count_success += 1
            except Exception as e:
                count_fail += 1
                print(f"转换失败: {str(e)}")
        else:
            count_skip += 1
            print(f"文件格式错误: {os.path.basename(file_path)} 不是 .webp 格式，跳过转换。")

        # 更新进度条
        progress_percentage = (i + 1) / total_files * 100
        progress_var.set(progress_percentage)
        progress_label.config(text=f"{progress_percentage:.2f}%")

    # 最终结果提示
    messagebox.showinfo("完成",
                        f"转换成功{count_success} 个文件！\n  转换失败{count_fail} 个文件！\n 转换跳过{count_skip} 个文件！")
    progress_var.set(0)
    progress_label.config(text="0.00%")


def convert_thread(input_files, output_folder, progress_var, progress_label):
    """
    使用线程来异步执行图片转换，避免阻塞主线程。
    """
    # 使用线程来执行转换
    threading.Thread(target=convert_webp_to_gif, args=(input_files, output_folder, progress_var, progress_label),
                     daemon=True).start()


def select_files():
    """
    选择要转换的 WebP 文件。
    """
    file_paths = filedialog.askopenfilenames(filetypes=[("WebP files", "*.webp")])
    if file_paths:
        listbox_files.delete(0, tk.END)
        for file_path in file_paths:
            listbox_files.insert(tk.END, file_path)


def remove_selected_file():
    """
    移除列表框中选定的文件。
    """
    selected_indices = listbox_files.curselection()
    for index in reversed(selected_indices):
        listbox_files.delete(index)


def select_output_folder():
    """
    选择输出文件夹。
    """
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, folder_path)


def start_conversion():
    """
    开始转换过程：
    """
    input_files = listbox_files.get(0, tk.END)
    output_folder = entry_output.get()

    if not input_files:
        messagebox.showwarning("选择文件", "请选择要转换的文件。")
        return

    if not output_folder:
        messagebox.showwarning("选择文件夹", "请选择输出文件夹。")
        return

    # 禁用所有按钮
    button_select_files.config(state=tk.DISABLED)
    button_remove_file.config(state=tk.DISABLED)
    button_select_output.config(state=tk.DISABLED)
    button_start.config(state=tk.DISABLED)

    progress_var.set(0)
    progress_label.config(text="0.00%")

    # 启动异步转换线程
    threading.Thread(target=convert_webp_to_gif_with_buttons, args=(input_files, output_folder, progress_var, progress_label)).start()

def convert_webp_to_gif_with_buttons(input_files, output_folder, progress_var, progress_label):
    """
    异步将 WebP 文件转换为 GIF 格式，并在转换完成后启用所有按钮。

    参数:
    - input_files: 要转换的 WebP 文件路径列表
    - output_folder: 转换后的文件保存路径
    - progress_var: 进度条变量，用于更新转换进度
    - progress_label: 标签变量，用于更新进度百分比文字
    """
    convert_webp_to_gif(input_files, output_folder, progress_var, progress_label)

    # 转换完成后启用所有按钮
    button_select_files.config(state=tk.NORMAL)
    button_remove_file.config(state=tk.NORMAL)
    button_select_output.config(state=tk.NORMAL)
    button_start.config(state=tk.NORMAL)

# 创建主窗口
root = tk.Tk()
root.title("WebP to GIF 转换工具")

# 获取屏幕的宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 设置窗口的尺寸
window_width = 600
window_height = 450

# 计算窗口的起始位置，使其居中显示
position_top = int((screen_height - window_height) / 2)
position_left = int((screen_width - window_width) / 2)

# 设置窗口的位置和大小
root.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

root.resizable(False, False)

# 文件选择
label_files = tk.Label(root, text="选择 WebP 文件:")
label_files.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

frame_files = tk.Frame(root)
frame_files.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W + tk.E)

scrollbar_files = tk.Scrollbar(frame_files, orient=tk.VERTICAL)
scrollbar_files.pack(side=tk.RIGHT, fill=tk.Y)

listbox_files = tk.Listbox(frame_files, width=60, height=10, yscrollcommand=scrollbar_files.set)
listbox_files.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_files.config(command=listbox_files.yview)

button_select_files = tk.Button(root, text="选择文件", command=select_files)
button_select_files.grid(row=2, column=0, padx=10, pady=10)

button_remove_file = tk.Button(root, text="移除选中文件", command=remove_selected_file)
button_remove_file.grid(row=2, column=1, padx=10, pady=10)

# 输出文件夹选择
label_output = tk.Label(root, text="选择输出文件夹:")
label_output.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

entry_output = tk.Entry(root, width=50)
entry_output.grid(row=3, column=1, padx=10, pady=10)

button_select_output = tk.Button(root, text="选择文件夹", command=select_output_folder)
button_select_output.grid(row=3, column=2, padx=10, pady=10)

# 开始转换按钮
button_start = tk.Button(root, text="开始转换", command=start_conversion)
button_start.grid(row=4, column=1, padx=10, pady=10)

# 进度条
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W + tk.E)

# 进度标签
progress_label = tk.Label(root, text="0.00%", bg='SystemButtonFace', bd=0)
progress_label.place(in_=progress_bar, relx=0.5, rely=0.5, anchor=tk.CENTER)

# 运行主循环
root.mainloop()
