import sys
import logging
from PySide6.QtWidgets import QApplication
from gui.main_window import SnapConvertApp

if __name__ == "__main__":
    # 配置日志记录
    logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s - %(message)s')
    app = QApplication(sys.argv)
    window = SnapConvertApp()
    window.show()
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\nexit")
        sys.exit(0)
