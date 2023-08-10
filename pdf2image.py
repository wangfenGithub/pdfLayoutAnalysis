import os

import fitz

def pdf_image(PDFDir,pdfPath, SaveDir, zoom_x, zoom_y, rotation_angle):
    """
    :param pdfPath: pdf文件的路径
    :param SaveDir: 图像要保存的文件夹
    :param zoom_x: x方向的缩放系数
    :param zoom_y: y方向的缩放系数
    :param rotation_angle: 旋转角度
    :return: None
    """
    # 打开PDF文件
    pdf = fitz.open(pdfPath)
    name = pdf.name
    print("in python name:{}".format(name))
    name = name.replace(PDFDir, '').replace('.pdf', '')
    print("in python name:{}".format(name))
    # 逐页读取PDF
    for pg in range(0, pdf.page_count):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        # 开始写图像
        pm.save(SaveDir + '/{}_'.format(name) + str(pg + 1) + ".jpg")
    pdf.close()


if __name__ == '__main__':
    pdf_dir_path = r".\PDF"
    saveDir = r".\PDF_Images"

    pdfs = os.listdir(pdf_dir_path)
    len_pdf = len(pdfs)
    k = 0
    for pdf in pdfs:
        k += 1
        pdf_path = os.path.join(pdf_dir_path, pdf)
        pdf_name = pdf.split(".")[0]  # pdf去除.后缀的文件名
        pdfImage_dir = os.path.join(saveDir, pdf_name)
        if os.path.exists(pdfImage_dir) == False:
            os.mkdir(pdfImage_dir)
        pdf_image(pdf_dir_path, pdf_path, pdfImage_dir, 4, 4, 0)