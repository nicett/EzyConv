import time
import os
import asyncio
import subprocess

import config
from converter.base_converter import Converter
# 创建信号量
semaphore = asyncio.Semaphore(config.CONCURRENCY_LIMIT)

class VideoConverter(Converter):
    def convert_file(self, file_path, output_path):
        pass

    def __init__(self, input_file, output_folder, target_format, progress_var, progress_label, progress_manager):
        super().__init__(input_file, output_folder, target_format, progress_var, progress_label)
        self.input_file = input_file
        self.output_folder = output_folder
        self.target_format = target_format
        self.progress_var = progress_var
        self.progress_label = progress_label
        self.progress_manager = progress_manager

    async def convert(self):
        start_time = time.time()

        base_name = os.path.basename(self.input_file)
        output_file = os.path.join(self.output_folder,os.path.splitext(base_name)[0] + f'.{self.target_format.lower()}')
        # 检查文件是否已存在，并生成唯一文件名
        output_file = self.get_unique_filename(output_file)
        print(f"开始转换 (async) at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}: {self.input_file} -> {output_file} (并发: {semaphore._value})")
        command = [
            'ffmpeg',
            '-i', self.input_file,
            '-c:v', 'copy',
            '-c:a', 'copy',
            output_file
        ]
        try:
            async with semaphore:  # 获取信号量
                process = await asyncio.create_subprocess_exec(
                    *command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                if process.returncode == 0:
                    print(f"转换完成 (async): {self.input_file} -> {output_file}")
                else:
                    print(f"转换 {self.input_file} 失败 (async): {stderr.decode()}")
        except Exception as e:
            print(f"转换 {self.input_file} 发生异常 (async): {e}")
        finally:
            end_time = time.time()
            duration = end_time - start_time
            print(f"转换耗时: {duration:.2f} 秒: {self.input_file} -> {output_file}")
        # total_files = len(self.input_files)
        # for i, file_path in enumerate(self.input_files):
        #     try:
        #
        #         base_name = os.path.basename(file_path)
        #         output_path = os.path.join(self.output_folder, os.path.splitext(base_name)[0] + f'.{self.target_format.lower()}')
        #         # 检查文件是否已存在，并生成唯一文件名
        #         output_path = self.get_unique_filename(output_path)
        #         ffmpeg.input(file_path).output(output_path,crf=0).run()
        #
        #
        #         # 更新进度条
        #         # self.progress_manager.update_progress(self.progress_var, self.progress_label, i, total_files)
        #
        #     except Exception as e:
        #         logging.error(f"转换失败: {file_path}，错误: {str(e)}")
        #         continue

    def update_progress(self, current_index):
        """
        更新进度条
        :param current_index:
        :return:
        """
        progress_percentage = (current_index + 1) / self.total_files * 100
        self.progress_var.set(progress_percentage)
        self.progress_label.config(text=f"{progress_percentage:.2f}%")