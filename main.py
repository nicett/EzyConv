import sys
import logging
from PySide6.QtWidgets import QApplication
from gui.main_window import SnapConvertApp

if __name__ == "__main__":
    # 配置日志记录
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    app = QApplication(sys.argv)
    window = SnapConvertApp()
    window.show()
    sys.exit(app.exec())
