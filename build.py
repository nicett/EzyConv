import platform
import shutil
import subprocess
import os
import sys


def find_path(env,exe):
    """
    Find the path of the ffmpeg executable file in the system.
    """
    path = os.environ.get(env)
    if path and shutil.which(path):
        return path

    executable = exe
    if platform.system() == 'Windows':
        executable = f'{exe}.exe'

    path = shutil.which(executable)
    return path


def run_command(command):

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        text=True
    )
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            print(line.strip())

    code = process.wait()
    return code


if __name__ == "__main__":
    ffmpeg_path = find_path("FFMPEG_PATH","ffmpeg")
    ffprobe_path = find_path("FFPROBE_PATH", "ffprobe")
    pyinstaller_command = [
        "pyinstaller",
        "-y",
        "--onefile",
        "--windowed",
        "--icon=assets/EzyConv.ico",
        "--add-data", "assets/*:assets",
        "--add-binary", f"{ffmpeg_path}:.",
        "--add-binary", f"{ffprobe_path}:.",
        "--name", "Ezy Conv",
        "main.py"
    ]

    print("Exec PyInstaller Command:")
    print(" ".join(pyinstaller_command))

    return_code = run_command(pyinstaller_command)
    if return_code == 0:
        print("The application has been successfully packaged!")
    else:
        print("Application packaging failed. Please check the error message.")