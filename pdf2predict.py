import argparse
import os
import fitz
import shutil
import yaml

import Extract_images_1
import SingleSidePDF2Json
import Extract_table_1



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
    name = name.replace(PDFDir, '').replace('.pdf', '')
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
    parser = argparse.ArgumentParser(description='Input file path,and the savepath')
    parser.add_argument(
        '--pdf_dir_path', type=str, help='the path of the pdf dir',
    )
    parser.add_argument(
        '--config_file_path',type=str,help='the path of the config dir'
    )
    parser.add_argument(
        '--yolo_data_dir', type=str, help='the path of the yolo inference image dir'
    )

    parser.add_argument(
        '--unit_change_path', type=str, help='the path of the yolo inference image dir'
    )
    parser.add_argument(
        '--extract_table', type=bool, default=False,help='if need extra table,set it with True'
    )
    parser.add_argument(
        '--extract_picture', type=bool, default=False, help='if need extra picture,set it with True'
    )
    parser.add_argument(
        '--extract_formula', type=bool, default=False, help='if need extra formula,set it with True'
    )
    parser.add_argument(
        '--extract_all', type=bool, default=True, help='if need extra all to json'
    )

    args = parser.parse_args()
    pdf_dir_path = args.pdf_dir_path
    config_file_path = args.config_file_path
    yolo_data_dir = args.yolo_data_dir
    unit_change_path = args.unit_change_path
    extract_table = args.extract_table
    extract_picture = args.extract_picture
    extract_formula = args.extract_formula
    extract_all = args.extract_all
    print("args")
    print(args)


    try:
        with open(config_file_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            file_path = data['path']
            command_str = data['command']
            yolo_label_dir = data['yolo_label_dir']
            yolo_detect_dir = data['yolo_detect_dir']
    except:
        print(None)

    # saveDir = r"/home/cloud/kantan/Bushu/PDF_Images"
    saveDir = os.path.join(file_path,'PDF_Images')
    # Predicted_Labels_path = r"/home/cloud/kantan/Bushu/All_Label/Labels"
    Predicted_Labels_path = os.path.join(file_path,'All_Label/Labels')

    pdfs = os.listdir(pdf_dir_path)
    len_pdf = len(pdfs)
    k = 0
    for pdf in pdfs:
        k += 1
        pdf_path = os.path.join(pdf_dir_path,pdf)
        pdf_name = pdf.split(".")[0]#pdf去除.pdf后缀的文件名
        pdfImage_dir = os.path.join(saveDir,pdf_name)
        if os.path.exists(pdfImage_dir) == False:
            os.mkdir(pdfImage_dir)
        pdf_image(pdf_dir_path, pdf_path, pdfImage_dir, 4, 4, 0)
        #
        images = os.listdir(pdfImage_dir)
        images_len = len(images)
        #将PDF对应的图片发送到服务器上
        # remote(pdfImage_dir, pdf_name)
        #将得到的图片文件复制到yolov7预测图片文件夹（yolo_data_dir）下边
        # yolo_data_dir = "/home/cloud/kantan/server/yolov7/inference/images"
        if os.path.exists(yolo_data_dir):
            shutil.rmtree(yolo_data_dir)
        os.mkdir(yolo_data_dir)

        for image_file in images:
            image_file_path = os.path.join(pdfImage_dir,image_file)
            shutil.copy(image_file_path,yolo_data_dir)

        if os.path.exists(yolo_detect_dir):
            shutil.rmtree(yolo_detect_dir)
        print("inference is starting")
        # command_str = "source /home/cloud/anaconda3/bin/activate kantan-server;cd /home/cloud/kantan/server/yolov7;python detect.py --weights /home/cloud/kantan/server/yolov7/weights/best.pt --source /home/cloud/kantan/server/yolov7/inference/images/ --save-txt --device 1 --conf-thres 0.35"
        os.system(command_str)
        print("inference ending")
        # 将预测结果复制到本地
        label_dir_path = os.path.join(Predicted_Labels_path, pdf_name)
        if os.path.exists(label_dir_path):
            shutil.rmtree(label_dir_path)
        os.mkdir(label_dir_path)


        yolo_detection_label_result = yolo_label_dir
        labels = os.listdir(yolo_detection_label_result)
        for label in labels:
            label_file = os.path.join(yolo_detection_label_result,label)
            # 把标签文件一个一个复制粘贴到本路径下的'All_Label/Labels/File1'下
            shutil.copy(label_file,label_dir_path)
        print("json starting")
        if extract_table:
            Extract_table_1.extract_table(config_file_path)
        if extract_picture:
            Extract_images_1.extract_image(config_file_path)
        if extract_all:
            SingleSidePDF2Json.PDFProcess(Predicted_Labels_path,file_path,unit_change_path)








