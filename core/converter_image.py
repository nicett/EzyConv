from PIL import Image
import logging

from core.converter import Converter


class ConverterImage(Converter):
    def convert_file(self, file_path, output_path):
        pass

    def __init__(self, input_file, output_file, target_format):
        super().__init__(input_file, output_file, target_format)
        self.input_file = input_file
        self.output_file = output_file
        self.target_format = target_format

    def convert(self):
        try:
            im = Image.open(self.input_file)
            im.save(self.output_file, self.target_format.lower(), save_all=True)
            logging.debug(f"成功 : {self.input_file} -> {self.output_file}")
            return True
        except Exception as e:
            logging.error(f"失败 : {self.input_file} 发生异常 : {e}")
            return False

