import os
import subprocess
import json
import sys
from typing import Dict, Optional
from utils.format_utils import format_size, format_duration

class MediaAnalyzer:
    @staticmethod
    def get_media_details(file_path: str) -> Dict[str, Optional[str]]:
        """
        使用 ffprobe 获取媒体文件的详细信息。

        参数:
            file_path: str，媒体文件的完整路径。

        返回:
            dict: 包含媒体文件详细信息的字典，包括以下键：
                - name: 文件名。
                - type: 文件类型（扩展名，如 "MP4", "JPG"）。
                - size: 文件大小（格式化后的字符串）。
                - resolution: 分辨率（如 "1920x1080"）。
                - duration: 时长（格式化后的字符串）。
                - full_path: 文件的完整路径。
                - error: 如果发生错误，则包含错误信息；否则为 None。
        """
        details = {
            "name": os.path.basename(file_path),
            "type": os.path.splitext(file_path)[1].upper().replace('.', ''),
            "size": "N/A",
            "resolution": "N/A",
            "duration": "N/A",
            "full_path": file_path,
            "error": None
        }

        try:
            # 尝试获取基本文件大小作为备用
            try:
                details["size"] = format_size(os.path.getsize(file_path))
            except OSError:
                pass



            # 构建 ffprobe 命令
            command = [
                "ffprobe",
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                file_path
            ]

            if sys.platform == "win32":
                creationflags = subprocess.CREATE_NO_WINDOW
            else:
                creationflags = 0


            # 执行 ffprobe 命令
            result = subprocess.run(command, capture_output=True, text=True, check=False, encoding='utf-8',creationflags=creationflags)

            if result.returncode != 0:
                error_msg = result.stderr or f"ffprobe exited with code {result.returncode}"
                if "No such file or directory" in error_msg or "Cannot open" in error_msg:
                    details["error"] = f"File not found or cannot be opened: {details['name']}"
                elif "Invalid data found when processing input" in error_msg:
                    details["error"] = f"Invalid data in file (corrupted?): {details['name']}"
                else:
                    details["error"] = f"ffprobe error processing file: {details['name']}. Details: {error_msg[:150]}"
                return details

            # 解析 JSON 输出
            media_info = json.loads(result.stdout)

            # 提取信息
            format_info = media_info.get('format', {})
            if 'duration' in format_info:
                details["duration"] = format_duration(format_info['duration'])
            if 'size' in format_info:
                details["size"] = format_size(format_info['size'])

            # 查找视频或图像流的分辨率
            stream_info = media_info.get('streams', [])
            for stream in stream_info:
                if stream.get('codec_type') == 'video':
                    if 'width' in stream and 'height' in stream:
                        details["resolution"] = f"{stream['width']}x{stream['height']}"
                        break
                elif stream.get('codec_type') == 'image':
                    if 'width' in stream and 'height' in stream:
                        if details["resolution"] == "N/A":
                            details["resolution"] = f"{stream['width']}x{stream['height']}"

        except FileNotFoundError:
            details["error"] = "ffprobe command not found. Please install FFmpeg."
        except json.JSONDecodeError:
            details["error"] = f"Failed to parse ffprobe output for {details['name']}."
        except Exception as e:
            details["error"] = f"An unexpected error occurred while processing {details['name']}: {str(e)}"

        # 对图片再次确认时长为 N/A
        if details["type"] in ["PNG", "JPG", "JPEG", "GIF", "WEBP", "BMP"] and details["duration"] != "N/A":
            details["duration"] = "N/A"

        return details
