import datetime
import pyheif
from PIL import Image
import os
import shutil
from tqdm import tqdm

# 获取当前日期时间
now = datetime.datetime.now()
datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")

# 创建目录
if not os.path.exists(f'heic_{datetime_str}'):
    os.mkdir(f'heic_{datetime_str}')
if not os.path.exists(f'heic-convert_{datetime_str}'):
    os.mkdir(f'heic-convert_{datetime_str}')

# 获取当前文件夹下的图片文件列表
files = os.listdir('.')
image_files = [file for file in files if file.endswith('.heic')]

# 初始化进度条
progress_bar = tqdm(total=len(image_files))

# 遍历每个图片文件
for image_file in image_files:
    # 图片文件路径
    src_path = os.path.abspath(image_file)

    # 新文件路径（修改文件后缀为.jpg）
    new_file_name = os.path.splitext(image_file)[0] + '.jpg'
    new_path = os.path.join(f'heic-convert_{datetime_str}', new_file_name)

    # 将HEIC文件转换为JPG，并保存为新文件
    heif_file = pyheif.read(src_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    image.save(new_path, format="JPEG")

    # 将原始文件移动到'heic'文件夹
    dst_path = os.path.join(f'heic_{datetime_str}', image_file)
    shutil.move(src_path, dst_path)

    # 更新进度条
    progress_bar.update(1)

# 关闭进度条
progress_bar.close()
