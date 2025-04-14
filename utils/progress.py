class ProgressManager:
    def update_progress(self, progress_var, progress_label, current_index, total_files):
        """
        更新进度条和进度文本
        :param progress_var: 进度条变量
        :param progress_label: 进度标签
        :param current_index: 当前文件索引
        :param total_files: 总文件数
        """
        progress_percentage = (current_index + 1) / total_files * 100
        progress_var.set(progress_percentage)
        progress_label.config(text=f"{progress_percentage:.2f}%")
