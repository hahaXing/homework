#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频编辑工具使用示例
演示如何使用VideoEditor类进行视频剪辑和拼接
"""

from video_editor import VideoEditor
import os

def example_clip_video():
    """视频剪辑示例"""
    print("=== 视频剪辑示例 ===")
    
    editor = VideoEditor()
    
    # 示例参数 - 请根据实际情况修改
    input_video = "input_4k_video.mp4"  # 输入的4K视频文件
    output_video = "clipped_video.mp4"   # 输出的剪辑视频
    start_time = 160.0  # 开始时间：30秒
    end_time = 165.0   # 结束时间：2分钟
    
    print(f"输入文件: {input_video}")
    print(f"输出文件: {output_video}")
    print(f"剪辑时间: {start_time}s - {end_time}s")
    
    # 执行剪辑
    success = editor.clip_video(
        input_path=input_video,
        output_path=output_video,
        start_time=start_time,
        end_time=end_time
    )
    
    if success:
        print("✓ 视频剪辑成功！")
    else:
        print("✗ 视频剪辑失败！")
    
    print()

def example_concatenate_videos():
    """视频拼接示例"""
    print("=== 视频拼接示例 ===")
    
    editor = VideoEditor()
    
    # 示例参数 - 请根据实际情况修改
    input_videos = [
        "video_part1.mp4",
        "video_part2.mp4",
        "video_part3.mp4"
    ]
    output_video = "merged_video.mp4"
    
    print(f"输入文件: {input_videos}")
    print(f"输出文件: {output_video}")
    
    # 执行拼接
    success = editor.concatenate_videos(
        input_paths=input_videos,
        output_path=output_video
    )
    
    if success:
        print("✓ 视频拼接成功！")
    else:
        print("✗ 视频拼接失败！")
    
    print()

def example_get_video_info():
    """获取视频信息示例"""
    print("=== 获取视频信息示例 ===")
    
    editor = VideoEditor()
    
    # 示例参数 - 请根据实际情况修改
    video_file = "sample_video.mp4"
    
    print(f"分析文件: {video_file}")
    
    # 获取视频信息
    info = editor.get_video_info(video_file)
    
    if info:
        print("视频信息:")
        print(f"  时长: {info['duration']:.2f} 秒 ({info['duration']/60:.1f} 分钟)")
        print(f"  帧率: {info['fps']:.2f} fps")
        print(f"  分辨率: {info['width']} x {info['height']}")
        print(f"  尺寸: {info['size']}")
        
        # 判断是否为4K视频
        if info['width'] >= 3840 and info['height'] >= 2160:
            print("  ✓ 这是一个4K视频")
        elif info['width'] >= 1920 and info['height'] >= 1080:
            print("  这是一个1080p视频")
        else:
            print("  这是一个标清视频")
    else:
        print("✗ 获取视频信息失败！")
    
    print()

def batch_process_example():
    """批量处理示例"""
    print("=== 批量处理示例 ===")
    
    editor = VideoEditor()
    
    # 批量剪辑多个视频的前60秒
    input_folder = "input_videos"  # 输入文件夹
    output_folder = "output_clips" # 输出文件夹
    clip_duration = 60.0  # 剪辑时长（秒）
    
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 处理文件夹中的所有MP4文件
    if os.path.exists(input_folder):
        for filename in os.listdir(input_folder):
            if filename.lower().endswith('.mp4'):
                input_path = os.path.join(input_folder, filename)
                output_filename = f"clip_{filename}"
                output_path = os.path.join(output_folder, output_filename)
                
                print(f"处理文件: {filename}")
                
                # 剪辑前60秒
                success = editor.clip_video(
                    input_path=input_path,
                    output_path=output_path,
                    start_time=0.0,
                    end_time=clip_duration
                )
                
                if success:
                    print(f"  ✓ 成功剪辑: {output_filename}")
                else:
                    print(f"  ✗ 剪辑失败: {filename}")
    else:
        print(f"输入文件夹不存在: {input_folder}")
    
    print()

def main():
    """主函数"""
    print("视频编辑工具使用示例")
    print("=" * 50)
    print()
    
    print("注意: 请根据实际情况修改示例中的文件路径")
    print()
    
    # 运行各种示例
    try:
        # 1. 视频剪辑示例
        example_clip_video()
        
        # 2. 视频拼接示例
        # example_concatenate_videos()
        
        # 3. 获取视频信息示例
        # example_get_video_info()
        
        # 4. 批量处理示例
        # batch_process_example()
        
    except ImportError:
        print("错误: 无法导入video_editor模块")
        print("请确保video_editor.py文件在同一目录下")
    except Exception as e:
        print(f"运行示例时发生错误: {str(e)}")
    
    print("示例演示完成！")
    print("\n使用提示:")
    print("1. 修改示例中的文件路径为实际的视频文件路径")
    print("2. 确保已安装所需依赖: pip install -r requirements.txt")
    print("3. 确保系统已安装FFmpeg")

if __name__ == "__main__":
    main()