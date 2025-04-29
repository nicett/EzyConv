# EzyConv - 简易媒体格式转换工具

![EzyConv](assets\EzyConv.ico)

EzyConv 是一个基于Python的媒体文件格式转换工具，支持图片和视频格式的快速转换。为了方便简单快速的转化，内置参数全部使用无损的方式。这只是一个开源的小工具、仅供娱乐。

视频处理基于：FFmpeg

图片处理基于：Pillow

## 功能特性
- 支持常见图片格式转换 (PNG, WEBP, GIF等)
- 支持视频格式转换 (MP4, AVI等)
- 多线程/异步处理提高转换效率
- 简洁易用的图形界面

## 安装

1. 确保已安装Python 3.8+
2. 克隆仓库:
   ```bash
   git clone https://github.com/yourusername/SnapConvert.git
   cd SnapConvert
   ```
3. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```
4. 确保已安装FFmpeg并添加到系统PATH

## 使用说明

### 命令行使用
```python
from core.converter import MediaConverter

converter = MediaConverter()
converter.convert_image('input.webp', 'output.gif')
converter.convert_video('input.mp4', 'output.avi')
```

### 图形界面
```bash
python main.py
```

### Windows
```bash
#  直接运行
./run.bat
```

### 构建可执行文件 .exe

#### 安装 pyinstaller
```bash
pip install pyinstaller
```
#### Windows下可直接运行构建脚本 或者 Python 运行 build.py
```bash
./build.bat 

# python build.py
```



## 项目结构
```
SnapConvert/
│
├── main.py                     # 应用程序入口点
├── requirements.txt            # 项目依赖
│
├── core/                       # 核心业务逻辑
│   ├── app.py                  # 主应用程序类
│   ├── converter.py            # 媒体转换核心类
│   ├── converter_factory.py    # 转换器工厂
│   ├── converter_image.py      # 图片转换实现
│   ├── converter_video.py      # 视频转换实现
│
├── gui/                        # 图形界面
│   ├── main_window.py          # 主窗口实现
│
├── backend/                    # 底层处理
│   ├── media_analyzer.py       # 媒体分析
│
├── config/                     # 配置管理
│   ├── config.py               # 应用配置
│
├── tests/                      # 测试
│   ├── test_asyncio.py         # 异步测试
│   ├── test_thread.py          # 多线程测试
│
└── utils/                      # 工具类
    ├── format_utils.py         # 格式处理工具
```

## 测试
运行所有测试:
```bash
python -m unittest discover tests
```

## 贡献
欢迎提交Pull Request。请确保:
1. 代码符合PEP8规范
2. 包含相应的测试用例
3. 更新相关文档

## 许可证
本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件
