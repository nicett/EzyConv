from abc import ABC, abstractmethod

# 抽象产品
class Converter(ABC):

    def __init__(self, input_file, output_folder, target_format):
        pass


    def validation(self):
        pass


    @abstractmethod
    def convert(self):
        pass


class MediaConverter:
    pass