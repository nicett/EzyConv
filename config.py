import os
# 定义并发限制大小
CONCURRENCY_LIMIT = os.cpu_count() or 4  # 默认限制为 CPU 核心数或 4

