import os
from PIL import Image

def compress_images(source_folder, output_folder, max_width=1080):
    # 如果输出目录不存在，创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历图片
    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(source_folder, filename)
            
            try:
                with Image.open(img_path) as img:
                    # 1. 解决手机照片旋转问题 (很多手机照片Exif里带有旋转信息)
                    from PIL import ImageOps
                    img = ImageOps.exif_transpose(img)

                    # 2. 计算缩放比例
                    # 即使是横屏图，限制宽度 1080 也足够手机看了
                    width_percent = (max_width / float(img.size[0]))
                    
                    # 如果图片本来就小于 max_width，就不放大了
                    if width_percent < 1:
                        h_size = int((float(img.size[1]) * float(width_percent)))
                        img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
                    
                    # 3. 保存并压缩 (质量设为 85 足够清晰)
                    output_path = os.path.join(output_folder, filename)
                    img.save(output_path, quality=85, optimize=True)
                    print(f"已处理: {filename}")
            except Exception as e:
                print(f"无法处理 {filename}: {e}")

# 运行
# 假设你的原图放在 raw_photos 文件夹里
# 处理好的图会放在 photos 文件夹里
if __name__ == "__main__":
    # 请先把你那些很大的原图放到一个叫 raw_photos 的文件夹里
    compress_images('raw_photos', 'photos')