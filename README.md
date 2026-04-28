# homework

这是一个用于保存 Python 学习作业和练习项目的仓库，当前主要包含数组练习、视频处理工具、中文词云程序，以及一个独立的黑客马拉松项目。

## 目录说明

### `homeWork_week1.py`

基础数组练习脚本，包含以下函数：

- `removeDuplicates(nums)`：删除有序数组中的重复元素
- `rotate(nums, k)`：将数组向右平移 `k` 位
- `twoSum(nums, target)`：查找和为目标值的两个下标
- `moveZeroes(nums)`：将数组中的 `0` 移动到末尾

运行方式：

```bash
python homeWork_week1.py
```

### `videoTools/`

视频处理相关脚本，主要功能包括：

- 视频剪辑
- 视频拼接
- 视频信息读取
- 视频抽帧
- 简单像素化处理

主要文件：

- `video_editor.py`：视频编辑核心程序
- `video_editor_example.py`：视频编辑示例脚本
- `video_trimmer.py`：视频裁剪工具
- `视频抽帧.py`：从视频中提取帧
- `像素化程序.py`：图像或视频像素化处理
- `批量删除绿幕背景.py`：批量删除图片绿幕背景，并输出透明 PNG

可能依赖：

- `moviepy`
- `ffmpeg`
- `pillow`
- `numpy`

示例运行：

```bash
python videoTools/video_editor_example.py
```

批量删除绿幕背景脚本运行方式：

```bash
python videoTools/批量删除绿幕背景.py
```

运行后会弹出文件夹选择框，程序会处理所选文件夹中的 `.jpg`、`.jpeg` 和 `.peg` 图片，并在同目录输出透明背景 PNG。

### `词云/`

中文文本处理与词云生成相关程序，包含文本分词、停用词过滤、Excel 文本导入和词云显示功能。

主要文件：

- `ciYun1.0.py`：带图形界面的词云程序
- `fenci.py`：文本分词与词云绘制示例
- `stopwords`、`哈工大停用词表.txt`：停用词文件
- `input.txt`、`input02.txt`：示例输入文本
- `image_file.jpg`：词云配色或形状参考图片

可能依赖：

- `jieba`
- `numpy`
- `pandas`
- `matplotlib`
- `wordcloud`
- `tkinter`

示例运行：

```bash
python 词云/ciYun1.0.py
```

### `黑客马拉松/`

这是一个相对独立的前后端项目，不属于基础作业脚本部分，目录中包含：

- `backend/`：Python 后端服务
- `frontend/`：前端界面

如果只查看作业内容，可以重点关注 `homeWork_week1.py`、`videoTools/` 和 `词云/`。

## 环境建议

- Python 3.10 及以上
- 部分脚本需要安装第三方库
- 视频处理脚本通常需要本机安装 `ffmpeg`

可以按需安装依赖，例如：

```bash
pip install moviepy pillow numpy jieba pandas matplotlib wordcloud
```

## 说明

- 仓库中的部分脚本是练习性质代码，运行前可能需要先修改输入文件路径
- 词云和视频处理程序依赖本地文件，建议在对应目录下运行
