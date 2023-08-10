import argparse
import os
import fitz
import shutil

import SingleSidePDF2Json

# hostname='10.16.33.155'
# username='wangfen'
# password='wangfen3090'
# port=22

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

#
# #远程执行终端命令
# def sshExeCMD(hostname,port,username,password):
#     client = paramiko.SSHClient()
#
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
#
#     client.connect(hostname,port,username,password)
#
#     print("正在开始进行预测")
#     command_str = "export PATH=/home/wangfen/anaconda3/bin:$PATH;cd /house/wangfen/Test/yolov7;python detect.py --weights /house/wangfen/Test/yolov7/runs/train/exp4/weights/best.pt --source /house/wangfen/Test/yolov7/myOwnData/images/ --save-txt --device 1 --conf-thres 0.35"
#
#     stdin, stdout, stderr = client.exec_command(command_str,get_pty=True)
#
#     client.close()
#
# def remote_scp(host_ip, remote_path, local_path, username, password):
#
#
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname,port,username,password)
#     stpf = paramiko.SFTPClient.from_transport(ssh.get_transport())
#     try:
#         stpf.get(remote_path, local_path)
#     except:
#         print(remote_path+"这个文件夹在预测结果中不存在，继续执行。。。。。。。。。")


if __name__ == '__main__':
    #下边是接受java项目那边传过来的参数，如果只在本地运行pdf转json程序，可以将下边参数接收注释掉
    parser = argparse.ArgumentParser(description='Input file path,and the savepath')
    parser.add_argument(
        'pdf_dir_path', type=str, help='the path of the pdf dir',
    )

    args = parser.parse_args()
    pdf_dir_path = args.pdf_dir_path
    saveDir = r"./PDF_Images"
    Predicted_Labels_path = r"./All_Label/Labels"

    pdfs = os.listdir(pdf_dir_path)
    len_pdf = len(pdfs)
    k = 0
    for pdf in pdfs:
        k += 1
        pdf_path = os.path.join(pdf_dir_path,pdf)
        pdf_name = pdf.split(".")[0]#pdf去除.后缀的文件名
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
        yolo_data_dir = "/house/yuanmingcai/kantan/yolov7/inference/images"
        if os.path.exists(yolo_data_dir):
            shutil.rmtree(yolo_data_dir)
        os.mkdir(yolo_data_dir)

        for image_file in images:
            image_file_path = os.path.join(pdfImage_dir,image_file)
            shutil.copy(image_file_path,yolo_data_dir)


        # # #传输图片完成，开始执行预测
        #预测之前删除detect文件夹下的exp文件夹
        # sshExeCMD(hostname, port, username, password)
        os.system("cmd")
        command_str = "source /house/yuanmingcai/anaconda3//bin/activate kantan-server;cd /house/yuanmingcai/kantan/yolov7;python detect.py --weights /house/yuanmingcai/kantan/yolov7/weights/best.pt --source /house/yuanmingcai/kantan/yolov7/inference/images/ --save-txt --device 1 --conf-thres 0.35"
        os.system(command_str)

        # 将预测结果复制到本地
        #
        label_dir_path = os.path.join(Predicted_Labels_path, pdf_name)
        if os.path.exists(label_dir_path):
            shutil.rmtree(label_dir_path)
        os.mkdir(label_dir_path)

        #再把标签文件一个一个复制粘贴过来
        yolo_detection_label_result = os.path.join(Predicted_Labels_path,pdf_path)
        labels = os.listdir(yolo_detection_label_result)
        for label in labels:
            label_file = os.path.join(yolo_detection_label_result,label)
            shutil.copy(label_file,label_dir_path)

        SingleSidePDF2Json.PDFProcess(Predicted_Labels_path)








