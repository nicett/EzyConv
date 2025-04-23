import pytest
import os
from unittest.mock import patch, MagicMock
from backend.media_analyzer import get_media_details
from gui.main_window import SnapConvertApp
from PySide6.QtWidgets import QApplication

@pytest.fixture
def app(qtbot):
    """Fixture for creating and returning the application instance."""
    application = SnapConvertApp()
    qtbot.addWidget(application)
    return application

class TestMediaAnalyzer:
    """Test cases for media analyzer functionality."""
    
    @patch('subprocess.run')
    def test_get_media_details_video(self, mock_run):
        """Test get_media_details with video file."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"format": {"duration": "120.5", "size": "1024000"}, "streams": [{"codec_type": "video", "width": 1920, "height": 1080}]}'
        mock_run.return_value = mock_result
        
        details = get_media_details("test.mp4")
        assert details["duration"] == "02:00"
        assert details["size"] == "1000.0 KB"
        assert details["resolution"] == "1920x1080"

    @patch('subprocess.run')
    def test_get_media_details_image(self, mock_run):
        """Test get_media_details with image file."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = '{"format": {"size": "512000"}, "streams": [{"codec_type": "image", "width": 800, "height": 600}]}'
        mock_run.return_value = mock_result
        
        details = get_media_details("test.jpg")
        assert details["duration"] == "N/A"
        assert details["size"] == "500.0 KB"
        assert details["resolution"] == "800x600"

class TestMainWindow:
    """Test cases for main window functionality."""
    
    def test_initial_state(self, app):
        """Test initial state of the application."""
        assert app.windowTitle() == "SnapConvert"
        assert app.file_table.rowCount() == 0
        assert not app.type_combo.isEnabled()

    @patch('PySide6.QtWidgets.QFileDialog.getOpenFileNames')
    def test_select_files(self, mock_dialog, app, qtbot):
        """Test file selection functionality."""
        mock_dialog.return_value = (["test1.jpg", "test2.png"], None)
        qtbot.mouseClick(app.file_button, Qt.LeftButton)
        assert app.file_table.rowCount() == 2

if __name__ == "__main__":
    pytest.main()
