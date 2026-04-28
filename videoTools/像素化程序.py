import os
from PIL import Image
from pathlib import Path

def crop_image(img, left=0, top=0, right=0, bottom=0):
    """
    固定像素裁剪（内部工具函数）
    """
    width, height = img.size
    new_left = left
    new_top = top
    new_right = width - right
    new_bottom = height - bottom

    if new_left >= new_right or new_top >= new_bottom:
        print("⚠️  裁剪参数过大，图片会被裁空，已跳过裁剪")
        return img

    cropped_img = img.crop((new_left, new_top, new_right, new_bottom))
    return cropped_img

def auto_crop_transparent(img, threshold=0):
    """
    【新增！】自动裁剪：检测透明区域，只保留有效像素
    :param img: Pillow图片
    :param threshold: 透明度阈值（0=只裁完全透明，越大裁得越多）
    :return: 自动裁剪后的图片
    """
    img = img.convert("RGBA")
    pixels = img.getdata()
    width, height = img.size

    left = width
    right = 0
    top = height
    bottom = 0

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[y * width + x]
            if a > threshold:
                left = min(left, x)
                right = max(right, x)
                top = min(top, y)
                bottom = max(bottom, y)

    # 安全判断
    if left > right or top > bottom:
        return img

    return img.crop((left, top, right + 1, bottom + 1))

def pixelate_image(img, pixel_size=10):
    """
    图片像素化
    """
    width, height = img.size
    small_img = img.resize((width // pixel_size, height // pixel_size), Image.NEAREST)
    pixelated_img = small_img.resize((width, height), Image.NEAREST)
    return pixelated_img

def process_image(
    input_path,
    output_path,
    left_crop=0,
    top_crop=0,
    right_crop=0,
    bottom_crop=0,
    pixel_size=0,
    auto_crop=False,        # 【新增开关】自动裁剪
    auto_threshold=0        # 【新增】自动裁剪灵敏度
):
    """
    统一处理：自动裁剪 + 固定裁剪 + 像素化
    """
    try:
        with Image.open(input_path) as img:
            processed_img = img.copy()

            # ============= 1. 【新增】自动裁剪（优先执行） =============
            if auto_crop:
                processed_img = auto_crop_transparent(processed_img, threshold=auto_threshold)

            # ============= 2. 固定像素裁剪 =============
            if left_crop > 0 or top_crop > 0 or right_crop > 0 or bottom_crop > 0:
                processed_img = crop_image(processed_img, left_crop, top_crop, right_crop, bottom_crop)

            # ============= 3. 像素化 =============
            if pixel_size > 0:
                processed_img = pixelate_image(processed_img, pixel_size)

            processed_img.save(output_path, "PNG")
            print(f"✅ 处理完成：{os.path.basename(input_path)}")

    except Exception as e:
        print(f"❌ 处理失败 {os.path.basename(input_path)}：{str(e)}")

def batch_process_png(
    folder_path,
    left_crop=0,
    top_crop=0,
    right_crop=0,
    bottom_crop=0,
    pixel_size=0,
    auto_crop=False,        # 【新增】开启自动裁剪
    auto_threshold=0
):
    folder = Path(folder_path)

    if not folder.exists():
        print(f"错误：文件夹 {folder_path} 不存在！")
        return

    output_folder = folder / "处理后_图片"
    output_folder.mkdir(exist_ok=True)

    png_files = list(folder.glob("*.png")) + list(folder.glob("*.PNG"))

    if not png_files:
        print("⚠️  文件夹中未找到任何PNG图片！")
        return

    print(f"📂 找到 {len(png_files)} 张PNG图片")
    if auto_crop:
        print(f"✅ 自动裁剪：开启（灵敏度={auto_threshold}）")
    else:
        print(f"✂️  固定裁剪：左={left_crop} 上={top_crop} 右={right_crop} 下={bottom_crop}")
    print(f"🎨 像素化大小：{pixel_size if pixel_size>0 else '关闭'}\n")

    for img_path in png_files:
        output_path = output_folder / img_path.name
        process_image(
            str(img_path),
            str(output_path),
            left_crop,
            top_crop,
            right_crop,
            bottom_crop,
            pixel_size,
            auto_crop=auto_crop,
            auto_threshold=auto_threshold
        )

    print(f"\n🎉 全部处理完成！文件保存在：{output_folder}")

# ====================== 使用者配置区域 ======================
if __name__ == "__main__":
    # ---------- 1. 文件夹路径 ----------
    TARGET_FOLDER = r"H:\游戏素材\毕设项目素材\建筑风格\场景"

    # ---------- 2. 【自动裁剪模式】 ----------
    AUTO_CROP = True               # ✅ 打开自动裁剪（会自动裁掉透明空白）
    AUTO_THRESHOLD = 0             # 灵敏度：0=严格裁透明，10=裁轻微透明

    # ---------- 3. 【固定裁剪】（自动裁剪开启后，这里建议都填0） ----------
    LEFT_CROP = 0
    TOP_CROP = 0
    RIGHT_CROP = 0
    BOTTOM_CROP = 0

    # ---------- 4. 像素化 ----------
    PIXEL_SIZE = 5   # 0=关闭

    # ========================================================

    # 执行批量处理
    batch_process_png(
        folder_path=TARGET_FOLDER,
        left_crop=LEFT_CROP,
        top_crop=TOP_CROP,
        right_crop=RIGHT_CROP,
        bottom_crop=BOTTOM_CROP,
        pixel_size=PIXEL_SIZE,
        auto_crop=AUTO_CROP,
        auto_threshold=AUTO_THRESHOLD
    )