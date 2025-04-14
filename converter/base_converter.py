# converter/base_converter.py
import os
import logging
from abc import ABC, abstractmethod

class Converter(ABC):
    def __init__(self, input_files, output_folder, target_format, progress_var, progress_label, compress=False):
        self.input_files = input_files
        self.output_folder = output_folder
        self.target_format = target_format
        self.progress_var = progress_var
        self.progress_label = progress_label
        self.compress = compress
        self.total_files = len(input_files)

    @abstractmethod
    def convert_file(self, file_path, output_path):
        pass

    def convert(self):
        for i, file_path in enumerate(self.input_files):
            try:
                base_name = os.path.basename(file_path)
                output_path = os.path.join(self.output_folder, os.path.splitext(base_name)[0] + f'.{self.target_format.lower()}')
                self.convert_file(file_path, output_path)
                logging.info(f"转换成功: {base_name} -> {output_path}")
                self.update_progress(i)
            except Exception as e:
                logging.error(f"转换失败: {file_path}，错误: {str(e)}")
                continue

    def update_progress(self, current_index):
        progress_percentage = (current_index + 1) / self.total_files * 100
        self.progress_var.set(progress_percentage)
        self.progress_label.config(text=f"{progress_percentage:.2f}%")
