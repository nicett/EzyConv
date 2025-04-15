class ProgressManager:
    def __init__(self):
        self.last_update = 0  # 上次更新进度的文件索引

    def update_progress(self, progress_var, progress_label, current_index, total_files):
        """
        更新进度条和进度文本，减少更新频率以提高性能。
        :param progress_var: 进度条变量
        :param progress_label: 进度标签
        :param current_index: 当前文件索引
        :param total_files: 总文件数
        """
        progress_percentage = (current_index + 1) / total_files * 100

        # 只在进度变化足够大时更新（例如每次更新超过1%）
        if abs(progress_percentage - self.last_update) >= 1:
            progress_var.set(progress_percentage)
            progress_label.config(text=f"{progress_percentage:.2f}%")
            self.last_update = progress_percentage  # 更新最后一次更新的进度

    def update_progress_threadsafe(self, progress_var, progress_label, current_index, total_files):
        """
        使用 Tkinter 的 after() 方法在主线程中更新进度条
        :param progress_var: 进度条变量
        :param progress_label: 进度标签
        :param current_index: 当前文件索引
        :param total_files: 总文件数
        """
        # 使用 after 确保更新操作在主线程中进行
        self.root.after(0, self.update_progress, progress_var, progress_label, current_index, total_files)
