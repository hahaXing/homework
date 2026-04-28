from moviepy.editor import VideoFileClip
import argparse


def trim_video(input_path, output_path, start_time, duration):
    """
    剪辑视频文件

    参数:
    input_path (str): 输入视频文件路径
    output_path (str): 输出视频文件路径
    start_time (float): 开始时间(秒)
    duration (float): 截取时长(秒)
    """
    try:
        # 加载视频文件
        with VideoFileClip(input_path) as video:
            # 计算结束时间
            end_time = start_time + duration

            # 确保结束时间不超过视频总时长
            if end_time > video.duration:
                end_time = video.duration
                print(f"警告: 截取时长超过视频总时长，将截取到视频末尾")

            # 剪辑视频
            trimmed_video = video.subclip(start_time, end_time)

            # 保存剪辑后的视频
            # codec参数指定编码器，可根据需要调整
            trimmed_video.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac"
            )

            print(f"视频剪辑完成，已保存至: {output_path}")

    except Exception as e:
        print(f"剪辑视频时出错: {str(e)}")


if __name__ == "__main__":
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='剪辑视频文件')
    parser.add_argument('input', help='输入视频文件路径')
    parser.add_argument('output', help='输出视频文件路径')
    parser.add_argument('start', type=float, help='开始时间(秒)')
    parser.add_argument('duration', type=float, help='截取时长(秒)')

    args = parser.parse_args()

    # 调用剪辑函数
    trim_video(args.input, args.output, args.start, args.duration)
