import logging
import subprocess
import sys

from core.converter import Converter

class ConverterVideo(Converter):


    def __init__(self, input_file, output_file, target_format):
        super().__init__(input_file, output_file, target_format)
        self.input_file = input_file
        self.output_file = output_file
        self.target_format = target_format


    def convert(self):

        command = [
            'ffmpeg',
            '-i', self.input_file,
            '-c:v', 'copy',
            '-c:a', 'copy',
            self.output_file
        ]

        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NO_WINDOW
        else:
            creationflags = 0

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=creationflags
            )
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                logging.debug(f"成功 : {self.input_file} -> {self.output_file}")
                return True
            else:
                logging.debug(f"失败 : {self.input_file}")
                return False
        except Exception as e:
            logging.error(f"失败 : {self.input_file} 发生异常: {e}")
            return False


