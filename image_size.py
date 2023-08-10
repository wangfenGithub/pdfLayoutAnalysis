from PIL import Image


def get_w(image_path):
    img = Image.open(image_path)
    imgSize = img.size  # 大小/尺寸
    w = img.width  # 图片的宽
    return w

def get_h(image_path):
    img = Image.open(image_path)
    imgSize = img.size  # 大小/尺寸
    h = img.height  # 图片的宽
    return h