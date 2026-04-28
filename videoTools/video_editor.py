#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频编辑工具
支持4K MP4视频的剪辑和拼接功能

依赖库:
- moviepy: pip install moviepy
- ffmpeg: 需要安装ffmpeg并添加到系统PATH
"""

import os
from moviepy import VideoFileClip, concatenate_videoclips
from typing import List, Tuple

class VideoEditor:
    """视频编辑器类"""
    
    def __init__(self):
        """初始化视频编辑器"""
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv']
    
    def validate_video_file(self, file_path: str) -> bool:
        """验证视频文件是否存在且格式支持
        
        Args:
            file_path: 视频文件路径
            
        Returns:
            bool: 文件是否有效
        """
        if not os.path.exists(file_path):
            print(f"错误: 文件不存在 - {file_path}")
            return False
        
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in self.supported_formats:
            print(f"错误: 不支持的文件格式 - {file_ext}")
            return False
        
        return True
    
    def clip_video(self, input_path: str, output_path: str, start_time: float, end_time: float) -> bool:
        """剪辑视频
        
        Args:
            input_path: 输入视频文件路径
            output_path: 输出视频文件路径
            start_time: 开始时间(秒)
            end_time: 结束时间(秒)
            
        Returns:
            bool: 是否成功
        """
        try:
            # 验证输入文件
            if not self.validate_video_file(input_path):
                return False
            
            print(f"开始剪辑视频: {input_path}")
            print(f"剪辑时间段: {start_time}s - {end_time}s")
            
            # 加载视频
            video = VideoFileClip(input_path)
            
            # 检查时间范围
            if start_time < 0 or end_time > video.duration or start_time >= end_time:
                print(f"错误: 时间范围无效. 视频总长度: {video.duration}s")
                video.close()
                return False
            
            # 剪辑视频
            clipped_video = video.subclipped(start_time, end_time)
            
            # 输出视频
            clipped_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            # 清理资源
            clipped_video.close()
            video.close()
            
            print(f"剪辑完成: {output_path}")
            return True
            
        except Exception as e:
            print(f"剪辑视频时发生错误: {str(e)}")
            return False
    
    def concatenate_videos(self, input_paths: List[str], output_path: str) -> bool:
        """拼接多个视频
        
        Args:
            input_paths: 输入视频文件路径列表
            output_path: 输出视频文件路径
            
        Returns:
            bool: 是否成功
        """
        try:
            if len(input_paths) < 2:
                print("错误: 至少需要2个视频文件进行拼接")
                return False
            
            # 验证所有输入文件
            for path in input_paths:
                if not self.validate_video_file(path):
                    return False
            
            print(f"开始拼接 {len(input_paths)} 个视频文件")
            
            # 加载所有视频
            video_clips = []
            for path in input_paths:
                print(f"加载视频: {path}")
                clip = VideoFileClip(path)
                video_clips.append(clip)
            
            # 拼接视频
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            # 输出视频
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            # 清理资源
            final_video.close()
            for clip in video_clips:
                clip.close()
            
            print(f"拼接完成: {output_path}")
            return True
            
        except Exception as e:
            print(f"拼接视频时发生错误: {str(e)}")
            return False
    
    def get_video_info(self, file_path: str) -> dict:
        """获取视频信息
        
        Args:
            file_path: 视频文件路径
            
        Returns:
            dict: 视频信息字典
        """
        try:
            if not self.validate_video_file(file_path):
                return {}
            
            video = VideoFileClip(file_path)
            info = {
                'duration': video.duration,
                'fps': video.fps,
                'size': video.size,
                'width': video.w,
                'height': video.h
            }
            video.close()
            
            return info
            
        except Exception as e:
            print(f"获取视频信息时发生错误: {str(e)}")
            return {}

def main():
    """主函数 - 使用示例"""
    editor = VideoEditor()
    
    print("=== 视频编辑工具 ===")
    print("支持功能:")
    print("1. 视频剪辑")
    print("2. 视频拼接")
    print("3. 获取视频信息")
    print()
    
    while True:
        print("请选择功能:")
        print("1 - 视频剪辑")
        print("2 - 视频拼接")
        print("3 - 获取视频信息")
        print("0 - 退出")
        
        choice = input("请输入选择 (0-3): ").strip()
        
        if choice == '0':
            print("退出程序")
            break
        
        elif choice == '1':
            # 视频剪辑
            input_path = input("请输入输入视频路径: ").strip()
            output_path = input("请输入输出视频路径: ").strip()
            
            try:
                start_time = float(input("请输入开始时间(秒): "))
                end_time = float(input("请输入结束时间(秒): "))
                
                success = editor.clip_video(input_path, output_path, start_time, end_time)
                if success:
                    print("✓ 剪辑成功!")
                else:
                    print("✗ 剪辑失败!")
                    
            except ValueError:
                print("错误: 请输入有效的时间数值")
        
        elif choice == '2':
            # 视频拼接
            print("请输入要拼接的视频文件路径 (每行一个，输入空行结束):")
            input_paths = []
            while True:
                path = input().strip()
                if not path:
                    break
                input_paths.append(path)
            
            if len(input_paths) < 2:
                print("错误: 至少需要2个视频文件")
                continue
            
            output_path = input("请输入输出视频路径: ").strip()
            
            success = editor.concatenate_videos(input_paths, output_path)
            if success:
                print("✓ 拼接成功!")
            else:
                print("✗ 拼接失败!")
        
        elif choice == '3':
            # 获取视频信息
            file_path = input("请输入视频文件路径: ").strip()
            info = editor.get_video_info(file_path)
            
            if info:
                print(f"视频信息:")
                print(f"  时长: {info['duration']:.2f} 秒")
                print(f"  帧率: {info['fps']:.2f} fps")
                print(f"  分辨率: {info['width']} x {info['height']}")
                print(f"  尺寸: {info['size']}")
            else:
                print("获取视频信息失败")
        
        else:
            print("无效选择，请重新输入")
        
        print()

if __name__ == "__main__":
    main()