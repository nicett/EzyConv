from PySide6.QtWidgets import (QApplication, QMainWindow,
                               QPushButton, QVBoxLayout,
                               QWidget, QLabel, QFileDialog)


class FolderSelector(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("文件夹选择示例")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("尚未选择文件夹")
        self.layout.addWidget(self.label)

        self.button = QPushButton("选择输出文件夹")
        self.button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.button)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择输出文件夹",
            "",
            QFileDialog.ShowDirsOnly
        )

        if folder_path:  # 如果用户没有取消选择
            self.label.setText(f"已选择文件夹: {folder_path}")


if __name__ == "__main__":
    app = QApplication([])
    window = FolderSelector()
    window.show()
    app.exec()