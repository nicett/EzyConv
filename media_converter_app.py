import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from converter.image_converter import ImageConverter
from converter.video_converter import VideoConverter
from utils.progress_manager import ProgressManager


class MediaConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("媒体格式转换工具")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.input_files = []
        self.output_folder = ""
        self.target_format = ""

        self.progress_manager = ProgressManager()

        self.create_widgets()

    def create_widgets(self):
        # 文件选择
        label_files = tk.Label(self.root, text="选择文件:")
        label_files.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        frame_files = tk.Frame(self.root)
        frame_files.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W + tk.E)

        scrollbar_files = tk.Scrollbar(frame_files, orient=tk.VERTICAL)
        scrollbar_files.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_files = tk.Listbox(frame_files, width=60, height=10, yscrollcommand=scrollbar_files.set)
        self.listbox_files.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_files.config(command=self.listbox_files.yview)

        button_select_files = tk.Button(self.root, text="选择文件", command=self.select_files)
        button_select_files.grid(row=2, column=0, padx=10, pady=10)

        button_remove_file = tk.Button(self.root, text="移除选中文件", command=self.remove_selected_file)
        button_remove_file.grid(row=2, column=1, padx=10, pady=10)

        # 输出文件夹选择
        label_output = tk.Label(self.root, text="选择输出文件夹:")
        label_output.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_output = tk.Entry(self.root, width=50)
        self.entry_output.grid(row=3, column=1, padx=10, pady=10)

        button_select_output = tk.Button(self.root, text="选择文件夹", command=self.select_output_folder)
        button_select_output.grid(row=3, column=2, padx=10, pady=10)

        # 格式选择
        label_format = tk.Label(self.root, text="选择目标格式:")
        label_format.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

        self.format_combobox = ttk.Combobox(self.root, values=["JPG", "PNG", "GIF", "WEBP", "MP4", "MOV", "AVI"])
        self.format_combobox.grid(row=4, column=1, padx=10, pady=10)

        # 开始转换按钮
        button_start = tk.Button(self.root, text="开始转换", command=self.start_conversion)
        button_start.grid(row=5, column=1, padx=10, pady=10)

        # 进度条
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        progress_bar.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W + tk.E)

        # 进度标签
        self.progress_label = tk.Label(self.root, text="0.00%", bg='SystemButtonFace', bd=0)
        self.progress_label.place(in_=progress_bar, relx=0.5, rely=0.5, anchor=tk.CENTER)

    def select_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("图片文件", "*.jpg;*.png;*.webp;*.gif"),
                                                            ("视频文件", "*.mp4;*.avi;*.mov;*.mkv")])
        if file_paths:
            self.listbox_files.delete(0, tk.END)
            for file_path in file_paths:
                self.listbox_files.insert(tk.END, file_path)

    def remove_selected_file(self):
        selected_indices = self.listbox_files.curselection()
        for index in reversed(selected_indices):
            self.listbox_files.delete(index)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.entry_output.delete(0, tk.END)
            self.entry_output.insert(0, folder_path)

    def start_conversion(self):
        self.input_files = self.listbox_files.get(0, tk.END)
        self.output_folder = self.entry_output.get()
        self.target_format = self.format_combobox.get()

        if not self.input_files:
            messagebox.showwarning("选择文件", "请选择要转换的文件。")
            return

        if not self.output_folder:
            messagebox.showwarning("选择文件夹", "请选择输出文件夹。")
            return

        if not self.target_format:
            messagebox.showwarning("选择格式", "请选择目标格式。")
            return

        # 禁用按钮
        self.disable_buttons()

        # 启动转换线程
        threading.Thread(target=self.convert_files).start()

    def convert_files(self):
        """
        根据目标格式转换文件。

        本函数根据目标格式(self.target_format)来决定使用哪种转换器（ImageConverter或VideoConverter）。
        它首先检查目标格式是否属于图像格式（'jpg', 'png', 'gif', 'webp'），如果是，则创建ImageConverter实例并调用其convert方法。
        如果目标格式属于视频格式（'mp4', 'avi', 'mov', 'mkv'），则创建VideoConverter实例并调用其convert方法。
        这两种转换器都需要输入文件列表、输出文件夹路径、目标格式以及进度变量和标签，以便在转换过程中更新进度信息。

        :return: 无返回值。
        """
        if self.target_format.lower() in ['jpg', 'png', 'gif', 'webp']:
            image_converter = ImageConverter(self.input_files, self.output_folder, self.target_format,
                                             self.progress_var, self.progress_label, self.progress_manager)
            image_converter.convert()
        elif self.target_format.lower() in ['mp4', 'avi', 'mov', 'mkv']:
            video_converter = VideoConverter(self.input_files, self.output_folder, self.target_format,
                                             self.progress_var, self.progress_label, self.progress_manager)
            video_converter.convert()

        # 转换完成后恢复按钮
        self.enable_buttons()

    def disable_buttons(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.DISABLED)

    def enable_buttons(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state=tk.NORMAL)