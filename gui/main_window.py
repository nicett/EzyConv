import os
import queue
import subprocess
import sys
from time import sleep

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QProgressBar,
    QTextEdit, QSizePolicy, QAbstractItemView, QCheckBox, QButtonGroup, QHeaderView
)
from PySide6.QtCore import Qt
from backend.media_analyzer import MediaAnalyzer
from core.app import App


class SnapConvertApp(QWidget):
    """
    主应用程序窗口类，提供文件选择、媒体信息显示和转换功能。
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EzyConv")
        self.setFixedSize(600, 800)
        # image_path = get_resource_path("assets/your_image.png")
        icon_path = self._get_resource_path("assets/EzyConv.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.setup_ui()
        self._check_ffprobe()

    def _get_resource_path(self,relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)



    def _check_ffprobe(self):
        """
        检查 ffprobe 是否可用。如果不可用，弹出警告对话框。
        """

        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NO_WINDOW
        else:
            creationflags = 0
        try:
            subprocess.run(["ffprobe", "-version"], capture_output=True, check=True, text=True, encoding='utf-8',creationflags=creationflags)
        except (FileNotFoundError, subprocess.CalledProcessError, OSError) as e:
            QMessageBox.warning(
                self,
                "依赖缺失",
                f"未能成功执行 `ffprobe` 命令。\n\n请确保您已正确安装 FFmpeg 并且 `ffprobe` 在系统的 PATH 环境变量中。\n\n文件详情（如分辨率、时长）功能将无法使用。\n错误: {e}"
            )

    def setup_ui(self):
        """
        设置用户界面，包括文件类型选择、文件表格、删除按钮、转换类型选择等功能。
        """
        layout = QVBoxLayout(self)

        # 文件类型选择
        check_layout = QHBoxLayout()
        self.image_checkbox = QCheckBox("选择图片文件")
        self.image_checkbox.setChecked(True)
        self.image_checkbox.toggled.connect(self.update_file_type)
        self.video_checkbox = QCheckBox("选择视频文件")
        self.video_checkbox.setChecked(False)
        self.video_checkbox.toggled.connect(self.update_file_type)
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.image_checkbox)
        self.button_group.addButton(self.video_checkbox)
        check_layout.addWidget(self.image_checkbox)
        check_layout.addWidget(self.video_checkbox)
        layout.addLayout(check_layout)

        # 文件选择按钮
        file_button_layout = QHBoxLayout()
        self.file_button = QPushButton("选择图片文件")
        self.file_button.clicked.connect(self.select_files)
        file_button_layout.addWidget(self.file_button)
        layout.addLayout(file_button_layout)

        # 文件详情表格
        layout.addWidget(QLabel("已选择文件:"))
        self.file_table = QTableWidget()
        self.file_table.setColumnCount(5)
        self.file_table.setHorizontalHeaderLabels(["名称", "类型", "大小", "分辨率", "时长"])
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.file_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.file_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.file_table.verticalHeader().setVisible(False)
        layout.addWidget(self.file_table)

        # 删除按钮
        delete_button = QPushButton("删除所选文件")
        delete_button.clicked.connect(self.delete_selected_files)
        layout.addWidget(delete_button)


        # 转换类型选择
        output_layout = QHBoxLayout()  # 创建一个水平布局
        self.file_output_label = QLabel("尚未选择文件夹")
        output_layout.addWidget(self.file_output_label)
        self.file_output_button = QPushButton("选择输出文件夹")
        self.file_output_button.clicked.connect(self.select_folder)
        output_layout.addWidget(self.file_output_button)
        layout.addLayout(output_layout)

        # 转换类型选择
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("转换类型:"))
        self.type_combo = QComboBox()
        self.type_combo.setEnabled(False)
        type_layout.addWidget(self.type_combo)
        layout.addLayout(type_layout)

        # 转换按钮
        self.convert_button = QPushButton("确认转换")
        self.convert_button.clicked.connect(self.confirm_conversion)
        layout.addWidget(self.convert_button)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # 详情切换
        self.toggle_detail_btn = QPushButton("收起详情")
        self.toggle_detail_btn.setCheckable(True)
        self.toggle_detail_btn.setChecked(True)
        self.toggle_detail_btn.toggled.connect(self.toggle_details)
        layout.addWidget(self.toggle_detail_btn)

        # 转换详情
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setVisible(True)
        self.detail_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.detail_text)

        self.update_file_type()

    def update_file_type(self):
        """
        更新当前选择的文件类型（图片或视频），并调整界面状态。
        """
        if self.image_checkbox.isChecked():
            self.selected_file_type = "image"
            self.file_button.setText("选择图片文件")
        elif self.video_checkbox.isChecked():
            self.selected_file_type = "video"
            self.file_button.setText("选择视频文件")
        else:
            self.selected_file_type = None
            self.file_button.setText("选择文件")
        self.update_convert_type()
        self.file_table.setRowCount(0)

    def update_convert_type(self):
        """
        根据当前选择的文件类型更新转换类型下拉菜单。
        """
        self.type_combo.clear()
        if self.selected_file_type == "image":
            self.type_combo.addItems(["PNG", "GIF", "WEBP"])
            self.type_combo.setEnabled(True)
        elif self.selected_file_type == "video":
            self.type_combo.addItems(["MP4", "AVI"])
            self.type_combo.setEnabled(True)
        else:
            self.type_combo.setEnabled(False)


    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择输出文件夹",
            "",
            QFileDialog.ShowDirsOnly
        )

        if folder_path:  # 如果用户没有取消选择
            self.file_output_label.setText(f"已选择文件夹: {folder_path}")
            # 将路径保存到成员变量中以便后续使用
            self.output_folder_path = folder_path
        else:
            # 用户点击了取消
            self.file_output_label.setText("尚未选择文件夹")
            self.output_folder_path = None

    def select_files(self):
        """
        打开文件选择对话框，选择文件并将其详细信息添加到表格中。
        """
        file_filter = "所有文件 (*)"
        if self.selected_file_type == "image":
            file_filter = "图片文件 (*.jpg *.jpeg *.png *.gif *.webp *.bmp)"
        elif self.selected_file_type == "video":
            file_filter = "视频文件 (*.mp4 *.avi *.mov *.mkv *.flv)"

        files, _ = QFileDialog.getOpenFileNames(
            self,
            f"选择{self.file_button.text().replace('选择', '').strip()}",
            "",
            file_filter
        )

        if files:
            current_files = set()
            for row in range(self.file_table.rowCount()):
                item = self.file_table.item(row, 0)
                if item:
                    full_path = item.data(Qt.UserRole)
                    if full_path:
                        current_files.add(full_path)

            new_files_added = 0
            QApplication.setOverrideCursor(Qt.WaitCursor)
            try:
                for file_path in files:
                    if file_path not in current_files:
                        details = MediaAnalyzer.get_media_details(file_path)

                        if details.get("error"):
                            QMessageBox.warning(self, "文件信息获取失败", f"无法获取文件 '{details['name']}' 的详细信息。\n原因: {details['error']}")

                        row_position = self.file_table.rowCount()
                        self.file_table.insertRow(row_position)

                        item_name = QTableWidgetItem(details["name"])
                        item_name.setData(Qt.UserRole, details["full_path"])

                        item_type = QTableWidgetItem(details["type"])
                        item_size = QTableWidgetItem(details["size"])
                        item_res = QTableWidgetItem(details["resolution"])
                        item_dur = QTableWidgetItem(details["duration"])

                        item_type.setTextAlignment(Qt.AlignCenter)
                        item_size.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        item_res.setTextAlignment(Qt.AlignCenter)
                        item_dur.setTextAlignment(Qt.AlignCenter)

                        self.file_table.setItem(row_position, 0, item_name)
                        self.file_table.setItem(row_position, 1, item_type)
                        self.file_table.setItem(row_position, 2, item_size)
                        self.file_table.setItem(row_position, 3, item_res)
                        self.file_table.setItem(row_position, 4, item_dur)

                        new_files_added += 1
                        QApplication.processEvents()

            finally:
                QApplication.restoreOverrideCursor()

            if new_files_added == 0 and len(files) > 0:
                QMessageBox.information(self, "提示", "所有选中的文件已在列表中。")

    def delete_selected_files(self):
        """
        删除表格中选中的文件行。
        """
        selected_rows = sorted([index.row() for index in self.file_table.selectionModel().selectedRows()], reverse=True)
        if not selected_rows:
            QMessageBox.information(self, "提示", "请先选择要删除的文件行。")
            return
        for row_index in selected_rows:
            self.file_table.removeRow(row_index)

    def confirm_conversion(self):
        """
        确认转换操作，弹出对话框让用户确认是否继续。
        """
        if self.file_table.rowCount() == 0:
            QMessageBox.warning(self, "未选择文件", "请先选择要转换的文件。")
            return

        if self.output_folder_path is None:
            QMessageBox.warning(self, "未选择输出文件夹", "请先选择输出文件夹。")
            return

        reply = QMessageBox.question(
            self, "确认转换", f"确定要将 {self.file_table.rowCount()} 个文件转换为 {self.type_combo.currentText()} 格式吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:

            self.start_conversion()

    def start_conversion(self):
        """
        开始转换过程，初始化进度条并模拟转换逻辑。
        """
        self.progress_bar.setValue(0)
        self.detail_text.clear()
        self.append_detail("开始转换...")

        self.files_to_convert = []

        for row in range(self.file_table.rowCount()):
            item = self.file_table.item(row, 0)
            if item:
                full_path = item.data(Qt.UserRole)
                if full_path:
                    self.files_to_convert.append(full_path)

        self.append_detail(f"目标格式: {self.type_combo.currentText()}")
        self.append_detail(f"文件数量: {len(self.files_to_convert)}")


        progress_queue = queue.Queue()
        App(self.output_folder_path, self.type_combo.currentText(),self.selected_file_type,progress_queue).convert(self.files_to_convert)

        step = 0
        count = len(self.files_to_convert)
        while not progress_queue.empty():
            task_msg = progress_queue.get()
            step += 1
            self.update_progress(step,count,task_msg)
            sleep(0.5)


    def update_progress(self,step:int,count:int,msg:str):

        progress = int((step / count) * 100)  # 使用 int() 截取小数部分
        self.progress_bar.setValue(progress)
        self.append_detail(f"{msg}")
        if step >= count:
            QMessageBox.information(self, "完成", "转换完成！")
        QApplication.processEvents()



    def toggle_details(self, checked):
        """
        切换转换详情文本框的可见性。
        """
        self.detail_text.setVisible(checked)
        self.toggle_detail_btn.setText("收起详情" if checked else "展开详情")

    def append_detail(self, text):
        """
        向转换详情文本框追加一行文本。
        """
        self.detail_text.append(text)
        self.detail_text.ensureCursorVisible()
