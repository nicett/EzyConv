# EzyConv - Simple Media Format Conversion Tool

![EzyConv](assets\EzyConv.ico)

EzyConv is a Python-based media file format conversion tool that supports fast conversion of image and video formats. For the sake of simplicity and speed, all built-in parameters use a lossless method. This is just a small open-source tool for entertainment purposes.

Video processing is based on: **FFmpeg**

Image processing is based on: **Pillow**

## Features
- Supports conversion of common image formats (PNG, WEBP, GIF, etc.)
- Supports conversion of video formats (MP4, AVI, etc.)
- Multi-threading/Asynchronous processing to improve conversion efficiency
- Simple and easy-to-use graphical user interface

## Installation

1. Ensure Python 3.8+ is installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/SnapConvert.git
   cd SnapConvert
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Ensure FFmpeg is installed and added to the system PATH.

## Usage

### Command Line Usage
```python
from core.converter import MediaConverter

converter = MediaConverter()
converter.convert_image('input.webp', 'output.gif')
converter.convert_video('input.mp4', 'output.avi')
```

### Graphical Interface
```bash
python main.py
```

### Windows
```bash
# Directly run
./run.bat
```

### Build Executable .exe

#### Install pyinstaller
```bash
pip install pyinstaller
```
#### On Windows, you can directly run the build script or use Python to run `build.py`:
```bash
./build.bat 

# python build.py
```

## Project Structure
```
SnapConvert/
│
├── main.py                     # Application entry point
├── requirements.txt            # Project dependencies
│
├── core/                       # Core business logic
│   ├── app.py                  # Main application class
│   ├── converter.py            # Media conversion core class
│   ├── converter_factory.py    # Converter factory
│   ├── converter_image.py      # Image conversion implementation
│   ├── converter_video.py      # Video conversion implementation
│
├── gui/                        # Graphical interface
│   ├── main_window.py          # Main window implementation
│
├── backend/                    # Backend processing
│   ├── media_analyzer.py       # Media analysis
│
├── config/                     # Configuration management
│   ├── config.py               # Application configuration
│
├── tests/                      # Tests
│   ├── test_asyncio.py         # Asynchronous tests
│   ├── test_thread.py          # Multi-threading tests
│
└── utils/                      # Utility classes
    ├── format_utils.py         # Format processing utilities
```

## Testing
To run all tests:
```bash
python -m unittest discover tests
```

## Contributing
Pull Requests are welcome. Please ensure:
1. Code follows PEP8 standards
2. Includes corresponding test cases
3. Updates relevant documentation

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.