# SnapConvert
Simple Media Format Converter

```
SnapConvert/
│
├── main.py                     # 应用程序入口点，初始化并运行App
│
├── core/                       # 核心业务逻辑和功能
│   ├── __init__.py
│   ├── app.py                  # 主应用程序类，协调GUI和后端
│   ├── converter.py            # 封装FFmpeg调用的核心类
│   ├── task_manager.py         # 管理转换任务队列、状态和进度 (多线程/异步处理)
│   ├── models.py               # 定义数据模型 (例如: ConversionJob, MediaInfo) - 可选但推荐
│   └── exceptions.py           # 自定义异常类
│
├── gui/                        # 图形用户界面相关
│   ├── __init__.py
│   ├── main_window.py          # 主窗口界面类 (例如: 基于 PyQt/PySide 或 Tkinter)
│   ├── widgets/                # 可复用的自定义UI控件 (例如: 文件选择器、进度条列表项)
│   │   ├── __init__.py
│   │   └── ...
│   ├── dialogs/                # 对话框 (例如: 设置、关于、错误提示)
│   │   ├── __init__.py
│   │   └── settings_dialog.py
│   └── utils.py                # GUI相关的辅助函数 (例如: 样式加载) - 可选
│
├── backend/                    # 底层交互 (在此项目中主要是FFmpeg)
│   ├── __init__.py
│   └── ffmpeg_handler.py       # 负责构建FFmpeg命令、执行进程、解析输出
│
├── config/                     # 配置管理
│   ├── __init__.py
│   └── settings.py             # 加载、保存应用程序设置 (FFmpeg路径, 输出目录等)
│
├── utils/                      # 通用工具类或函数
│   ├── __init__.py
│   └── logger.py               # 日志记录配置
│   └── file_helper.py          # 文件操作辅助
│
├── assets/                     # 静态资源 (图标、样式表等) - 可选
│   └── icons/
│       └── app_icon.png
│
├── tests/                      # 单元测试和集成测试 (推荐)
│   ├── __init__.py
│   └── test_converter.py       # 针对 core.converter 的测试
│   └── ...
│
├── requirements.txt            # 项目依赖库列表
└── README.md                   # 项目说明文档
```
