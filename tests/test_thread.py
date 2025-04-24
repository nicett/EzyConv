import subprocess
import time
import os
import os.path
from concurrent.futures import ThreadPoolExecutor, as_completed


# 定义并发限制大小
CONCURRENCY_LIMIT = os.cpu_count() or 4  # 默认限制为 CPU 核心数或 4

# 创建线程池
executor = ThreadPoolExecutor(max_workers=CONCURRENCY_LIMIT)


# 定义一个函数，用于转换文件格式
def convert_file(input_file, output_file):
    """
    转换文件格式，从输入文件到输出文件
    :param input_file: 需要转换的输入文件路径
    :param output_file: 转换后的输出文件路径
    """
    start_time = time.time()
    print(
        f"开始转换 (thread) at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}: {input_file} -> {output_file}")
    command = [
        'ffmpeg',
        '-i', input_file,
        '-c:v', 'copy',
        '-c:a', 'copy',
        output_file
    ]
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print(f"转换完成 (thread): {input_file} -> {output_file}")
        else:
            print(f"转换 {input_file} 失败 (thread): {stderr.decode()}")
    except Exception as e:
        print(f"转换 {input_file} 发生异常 (thread): {e}")
    finally:
        end_time = time.time()
        duration = end_time - start_time
        print(f"转换耗时: {duration:.2f} 秒: {input_file} -> {output_file}")


# 定义主函数，使用线程池执行多个文件转换任务
def main():
    start_time_total = time.time()
    print(
        f"程序开始运行 at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time_total))}, 并发限制: {CONCURRENCY_LIMIT}")

    input_files = [
        r'input-1.mp4',
        r'input-2.mp4',
        r'input-3.mp4',
        r'input-4.mp4',
        r'input-5.mp4',
        # 可以添加更多文件进行测试
    ]
    output_files = [
        'output1_pooled.mkv',
        'output2_pooled.mkv',
        'output3_pooled.mkv',
        'output4_pooled.mkv',
        'output5_pooled.mkv',
        # 对应更多输出文件名
    ]



    # 提交任务到线程池
    futures = []
    for i in range(len(input_files)):
        if os.path.isfile(input_files[i]):
            future = executor.submit(convert_file, input_files[i], output_files[i])
            futures.append(future)


    if len(futures) != 0:
    # 等待所有任务完成
        for future in as_completed(futures):
            pass  # 可以根据需要捕获异常

    end_time_total = time.time()
    total_duration = end_time_total - start_time_total
    print(
        f"所有文件转换完成 (thread) at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time_total))}, 总耗时: {total_duration:.2f} 秒")


# 程序入口，运行主函数
if __name__ == "__main__":
    main()
