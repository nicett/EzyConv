import logging
import queue
import time
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.converter_factory import ConverterFactory


class App:
    # 定义并发限制大小
    CONCURRENCY_LIMIT = os.cpu_count() or 4  # 默认限制为 CPU 核心数或 4

    def __init__(self, output_folder, combo,type,progress_queue: queue.Queue):
        self.output_folder = output_folder
        self.combo = combo
        self.type = type
        self.progress_queue = progress_queue
        self.executor = ThreadPoolExecutor(max_workers=self.CONCURRENCY_LIMIT)

    @staticmethod
    def get_unique_filename(output_path):
        """
        生成一个唯一的文件名，避免覆盖已有文件。
        :param output_path: 初步生成的文件路径
        :return: 唯一的文件路径
        """
        base, extension = os.path.splitext(output_path)
        counter = 1

        # 如果文件已经存在，增加编号直到文件名唯一
        while os.path.exists(output_path):
            output_path = f"{base}_{counter}{extension}"
            counter += 1

        # 统一为正向斜杠
        path_obj = Path(output_path)
        uniform_path = path_obj.as_posix()  # 转换为正斜杠

        # 或者统一为反斜杠
        # uniform_path = str(path_obj)  # 转换为系统

        return uniform_path

    def _start(self,input_file):

        base_name = os.path.basename(input_file)
        output_file = os.path.join(self.output_folder, os.path.splitext(base_name)[0] + f'.{self.combo.lower()}')
        # 检查文件是否已存在，并生成唯一文件名
        output_file = self.get_unique_filename(output_file)

        converter = ConverterFactory.create_converter(input_file=input_file, output_file=output_file,target_format=self.combo.lower(), converter_type=self.type)

        if converter.convert():
            self.progress_queue.put(f"成功: {input_file} -> {output_file}")
        else:
            self.progress_queue.put(f"失败: {input_file} -> {output_file}")


    def convert(self, input_files):
        """
        使用线程池执行多个文件转换任务
        :param input_files: 需要转换的输入文件列表
        """
        start_time_total = time.time()
        logging.debug(f"程序开始运行 at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time_total))}, 并发限制: {self.CONCURRENCY_LIMIT}")
        # 提交任务到线程池
        futures = []
        for input_file in input_files:
            future = self.executor.submit(self._start, input_file)
            futures.append(future)

        # 等待所有任务完成
        for future in as_completed(futures):
            if exception := future.exception():
                logging.error(f"任务执行时发生异常: {exception}")

        end_time_total = time.time()
        total_duration = end_time_total - start_time_total
        logging.debug(f"所有文件转换完成 (thread) at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time_total))}, 总耗时: {total_duration:.2f} 秒")