import math

def format_size(size_bytes):
    """
    将字节大小格式化为可读的字符串 (KB, MB, GB)。

    参数:
        size_bytes: int 或 None，表示文件大小的字节数。如果为 None，则返回 "N/A"。

    返回:
        str: 格式化后的文件大小字符串，例如 "1.23 MB"。
    """
    if size_bytes is None:
        return "N/A"
    try:
        size_bytes = int(size_bytes)
        if size_bytes == 0:
            return "0 B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        if i >= len(size_name): i = len(size_name) - 1
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
    except (ValueError, TypeError):
        return "N/A"

def format_duration(seconds_str):
    """
    将秒（可能为字符串形式）格式化为 HH:MM:SS 或 MM:SS。

    参数:
        seconds_str: str 或 float，表示时长的秒数。可以是字符串形式的数字。

    返回:
        str: 格式化后的时长字符串，例如 "01:23:45" 或 "23:45"。
    """
    try:
        seconds = float(seconds_str)
        if seconds < 0:
            return "N/A"
        total_seconds = int(seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    except (ValueError, TypeError, AttributeError):
        return "N/A"
