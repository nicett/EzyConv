import argparse
from converter.image_converter import ImageConverter
from converter.video_converter import VideoConverter

def main():
    parser = argparse.ArgumentParser(description="图片视频格式转换工具")
    parser.add_argument("files", nargs='+', help="输入文件路径")
    parser.add_argument("output", help="输出文件夹路径")
    parser.add_argument("format", help="目标格式，例如 'jpg', 'mp4'")

    args = parser.parse_args()

    if args.format.lower() in ['jpg', 'png', 'gif', 'webp']:
        ImageConverter(args.files, args.output, args.format, None, None)
    elif args.format.lower() in ['mp4', 'avi', 'mov', 'mkv']:
        VideoConverter(args.files, args.output, args.format, None, None)

if __name__ == "__main__":
    main()
