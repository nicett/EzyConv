import ffmpeg




# 显式指定 FFmpeg 可执行文件的路径
# ffmpeg.input(r'C:\Users\zhaoz\Desktop\测试图片\thailand-1.mp4').output(r'C:\Users\zhaoz\Desktop\测试图片\转化后\output.avi').run()

try:
    ffmpeg.input(r'C:\Users\zhaoz\Desktop\测试图片\thailand-1.mp4').output('output.avi',vcodec = 'copy').run()
except ffmpeg.Error as e:
    print(f"转换失败！错误信息: {e.stderr.decode('utf8')}")
#
# ffmpeg.input(r'C:\Users\zhaoz\Desktop\测试图片\thailand.mp4').copy('output.avi').run()

##无损转法
# ffmpeg -i C:\Users\zhaoz\Desktop\测试图片\IMG_5014.MP4 -c:v copy -c:a copy output.mkv

### 无法无损转换 请继续调试