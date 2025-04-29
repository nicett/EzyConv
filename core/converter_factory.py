# 简单工厂
from core.converter import Converter
from core.converter_image import ConverterImage
from core.converter_video import ConverterVideo


class ConverterFactory:
    @staticmethod
    def create_converter(input_file, output_file, target_format, converter_type) -> Converter:
        if converter_type == "image":
            return ConverterImage(input_file, output_file, target_format)
        elif converter_type == "video":
            return ConverterVideo(input_file, output_file, target_format)
        else:
            raise ValueError(f"Unknown converter type: {converter_type}")