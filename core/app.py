import subprocess
import time
import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定义并发限制大小
CONCURRENCY_LIMIT = os.cpu_count() or 4  # 默认限制为 CPU 核心数或 4

# 创建线程池
executor = ThreadPoolExecutor(max_workers=CONCURRENCY_LIMIT)


def get_unique_filename(output_path):
    """
    生成一个唯一的文件名，避免覆盖已有文件。
    :param output_path: 初步生成的文件路径
    :return: 唯一的文件路径
    """
    base, extension = os.path.splitext(output_path)
    counter = 1

    # 如果文件已经存在，增加编号直到文件名唯一
    while os.path.exists(output_path):
        output_path = f"{base}_{counter}{extension}"
        counter += 1

    return output_path

# 定义一个函数，用于转换文件格式
def convert_file(input_file, output_folder,combo):
    """
    转换文件格式，从输入文件到输出文件
    :param input_file: 需要转换的输入文件路径
    :param output_file: 转换后的输出文件路径
    """
    start_time = time.time()
    base_name = os.path.basename(input_file)
    output_file = os.path.join(output_folder, os.path.splitext(base_name)[0] + f'.{combo.lower()}')

    # 检查文件是否已存在，并生成唯一文件名
    output_file = get_unique_filename(output_file)

    print(f"开始转换 (thread) at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}: {input_file} -> {output_file}")

    end_time = time.time()
    duration = end_time - start_time

    if combo not in ['mp4','avi']:
        im = Image.open(input_file)
        im.save(output_file, combo.lower(),save_all=True)
        print(f"转换完成 (thread): {input_file} -> {output_file}")
        print(f"转换耗时: {duration:.2f} 秒: {input_file} -> {output_file}")
        return

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
        print(f"转换耗时: {duration:.2f} 秒: {input_file} -> {output_file}")


# 定义主函数，使用线程池执行多个文件转换任务
def convert(input_files,output_folder,combo):
    start_time_total = time.time()
    print(f"程序开始运行 at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time_total))}, 并发限制: {CONCURRENCY_LIMIT}")

    # input_files = [
    #     r'C:\Users\zhaoz\Desktop\测试图片\thailand-1.mp4',
    #     r'C:\Users\zhaoz\Desktop\测试图片\thailand-2.mp4',
    #     r'C:\Users\zhaoz\Desktop\测试图片\thailand-3.mp4',
    #     r'C:\Users\zhaoz\Desktop\测试图片\thailand-4.mp4',
    #     r'C:\Users\zhaoz\Desktop\测试图片\thailand-5.mp4',
    #     # 可以添加更多文件进行测试
    # ]
    # output_files = [
    #     'output1_threaded.mkv',
    #     'output2_threaded.mkv',
    #     'output3_threaded.mkv',
    #     'output4_threaded.mkv',
    #     'output5_threaded.mkv',
    #     # 对应更多输出文件名
    # ]

    # 提交任务到线程池
    futures = []
    for i in range(len(input_files)):
        future = executor.submit(convert_file, input_files[i], output_folder,combo)
        futures.append(future)

    # 等待所有任务完成
    for future in as_completed(futures):
        pass  # 可以根据需要捕获异常

    end_time_total = time.time()
    total_duration = end_time_total - start_time_total
    print(f"所有文件转换完成 (thread) at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time_total))}, 总耗时: {total_duration:.2f} 秒")

