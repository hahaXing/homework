import os
from pathlib import Path
from tkinter import Tk, filedialog, messagebox

import numpy as np
from PIL import Image, ImageFilter


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
OUTPUT_FOLDER_NAME = "去绿幕输出_PNG"

# 下面几个参数决定绿幕识别的宽松程度，可按需要微调。
GREEN_DOMINANCE = 25
MIN_GREEN = 60
EDGE_SOFTNESS = 1.2


def select_folder():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    folder = filedialog.askdirectory(title="选择包含绿幕图片的文件夹")
    root.destroy()
    return folder


def find_image_files(folder_path):
    folder = Path(folder_path)
    image_files = []
    for item in folder.iterdir():
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
            image_files.append(item)
    return sorted(image_files)


def remove_green_screen(image):
    rgba = image.convert("RGBA")
    data = np.array(rgba, dtype=np.uint8)

    red = data[:, :, 0].astype(np.int16)
    green = data[:, :, 1].astype(np.int16)
    blue = data[:, :, 2].astype(np.int16)

    green_mask = (
        (green > MIN_GREEN)
        & (green - red > GREEN_DOMINANCE)
        & (green - blue > GREEN_DOMINANCE)
    )

    alpha = np.where(green_mask, 0, 255).astype(np.uint8)
    data[:, :, 3] = alpha

    result = Image.fromarray(data, mode="RGBA")

    # 轻微模糊 alpha 边缘，减少硬边和部分绿边残留。
    alpha_image = result.getchannel("A").filter(ImageFilter.GaussianBlur(radius=EDGE_SOFTNESS))
    result.putalpha(alpha_image)
    return result


def build_output_path(output_folder, input_path):
    return output_folder / f"{input_path.stem}.png"


def process_folder(folder_path):
    image_files = find_image_files(folder_path)
    if not image_files:
        messagebox.showwarning(
            "未找到图片",
            "所选文件夹中没有找到 .jpg、.jpeg 或 .png 图片。"
        )
        return

    output_folder = Path(folder_path) / OUTPUT_FOLDER_NAME
    output_folder.mkdir(exist_ok=True)

    success_count = 0
    failed_files = []

    for image_path in image_files:
        try:
            with Image.open(image_path) as image:
                result = remove_green_screen(image)
                output_path = build_output_path(output_folder, image_path)
                result.save(output_path, "PNG")
                success_count += 1
                print(f"已处理: {image_path.name} -> {output_path.name}")
        except Exception as exc:
            failed_files.append(f"{image_path.name}: {exc}")
            print(f"处理失败: {image_path.name} - {exc}")

    message = (
        f"处理完成。\n\n"
        f"成功: {success_count} 张\n"
        f"失败: {len(failed_files)} 张\n"
        f"输出目录: {output_folder}"
    )

    if failed_files:
        preview = "\n".join(failed_files[:5])
        if len(failed_files) > 5:
            preview += "\n..."
        message += f"\n\n失败详情:\n{preview}"

    messagebox.showinfo("批量删除绿幕背景", message)


def main():
    folder_path = select_folder()
    if not folder_path:
        print("未选择文件夹，程序已取消。")
        return

    process_folder(folder_path)


if __name__ == "__main__":
    main()
