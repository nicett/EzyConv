import tkinter as tk
import logging
from media_converter_app import MediaConverterApp







if __name__ == "__main__":
    root = tk.Tk()
    app = MediaConverterApp(root)
    # 配置日志记录
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    root.mainloop()
