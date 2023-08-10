# -*- coding: UTF-8 -*-
import os.path

from PIL import Image
from PIL import ImageEnhance

# crops_path = r".\crops\temp.jpg"
# crops_path = r"D:\codeMyself\pythonProject\kantanyuan_Bushu - 1\crops\temp.jpg"
def Enhancement(file_path):
    # 原始图像
    crops_path = os.path.join(file_path,'crops/temp.jpg')
    image = Image.open(crops_path)


    # 锐度增强
    enh_sha = ImageEnhance.Sharpness(image)
    sharpness = 3.0
    image_sharped = enh_sha.enhance(sharpness)
    # image_sharped.show()
    # save_path = r"D:\codeMyself\pythonProject\kantanyuan_Bushu - 1\test.jpg"
    save_path = os.path.join(file_path,'test.jpg')
    image_sharped.save(save_path)
    return True
