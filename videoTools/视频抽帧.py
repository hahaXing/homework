import cv2
import os
from tkinter import Tk, filedialog, simpledialog, messagebox


def _safe_imwrite(file_path, image):
    ext = os.path.splitext(file_path)[1] or ".jpg"
    ok, buf = cv2.imencode(ext, image)
    if not ok:
        return False
    try:
        with open(file_path, "wb") as f:
            f.write(buf.tobytes())
        return True
    except OSError:
        return False


def extract_frames(video_path, num_frames=30):
    """
    从视频中均匀抽取指定数量的帧
    """
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        messagebox.showerror("错误", "无法打开视频文件！")
        return False
    
    # 获取视频信息
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0
    
    # 检查视频长度是否大于1秒
    if duration <= 1:
        messagebox.showerror("错误", f"视频长度必须大于1秒！当前视频长度: {duration:.2f}秒")
        cap.release()
        return False
    
    # 创建输出目录
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(os.path.dirname(video_path), f"{video_name}_frames_{num_frames}")
    os.makedirs(output_dir, exist_ok=True)
    
    # 计算抽帧间隔
    interval = total_frames / num_frames
    
    extracted_count = 0
    read_failed = 0
    write_failed = 0
    for i in range(num_frames):
        # 计算目标帧位置
        target_frame = int(i * interval)
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        
        ret, frame = cap.read()
        if ret and frame is not None:
            # 保存帧为图片
            frame_filename = os.path.join(output_dir, f"frame_{i+1:04d}.jpg")
            if _safe_imwrite(frame_filename, frame):
                extracted_count += 1
            else:
                write_failed += 1
        else:
            read_failed += 1
    
    cap.release()
    
    if extracted_count == 0:
        messagebox.showerror(
            "未生成输出",
            "未能保存任何图片。\n\n"
            f"视频路径: {video_path}\n"
            f"输出目录: {output_dir}\n"
            f"total_frames: {total_frames}\n"
            f"fps: {fps}\n"
            f"读帧失败: {read_failed}\n"
            f"写入失败: {write_failed}\n\n"
            "建议：\n"
            "1) 把视频放到纯英文路径下再试\n"
            "2) 确认输出目录不在只读/无权限位置\n"
            "3) 如果是 HEVC/H265 等编码，尝试换成 H264 的 mp4"
        )
        return False

    messagebox.showinfo(
        "完成",
        f"成功抽取 {extracted_count} 帧！\n"
        f"保存位置: {output_dir}\n"
        f"读帧失败: {read_failed}\n"
        f"写入失败: {write_failed}"
    )
    return True


def main():
    # 创建Tkinter根窗口（隐藏）
    root = Tk()
    root.withdraw()
    
    # 选择视频文件
    video_path = filedialog.askopenfilename(
        title="选择MP4视频文件",
        filetypes=[("MP4视频", "*.mp4"), ("所有文件", "*.*")]
    )
    
    if not video_path:
        return
    
    # 选择抽帧数量
    num_frames = simpledialog.askinteger(
        "选择抽帧数量",
        "请输入要抽取的帧数（30 或 60）：",
        initialvalue=30,
        minvalue=1,
        maxvalue=1000
    )
    
    if num_frames is None:
        return
    
    # 执行抽帧
    extract_frames(video_path, num_frames)
    
    root.destroy()


if __name__ == "__main__":
    main()
