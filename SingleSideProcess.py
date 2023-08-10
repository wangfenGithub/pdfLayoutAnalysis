import os

import yaml
from PIL import Image
import easyocr
# import formulaTest
import image_size
import cv2
import Enhancement_Test
import TableProcess


def SingleSidePageProcess(label_file_path,label_file_name,img_path,PDF_name,page_num,PDF_path,file_path,unit_change_path):
    """
    :param label_file_path: 标签文件的路径,例如：D:\pythonProject\yolov7Process\All_Label\dizhi\File1_1.txt
    :param label_file_name: File1_1
    :param img_path: 图片路径，D:\pythonProject\yolov7Process\PDF_Imagesl\File1\File1_1.jpg
    :param PDF_name:
    :param page_num:
    :param PDF_path: D:\pythonProject\yolov7Process\PDFl\File1.pdf
    :param file_path:
    :param unit_change_path:单位配置文件路径
    :return:
    """
    crops_path = os.path.join(file_path,"crops/temp.jpg")
    Formula_path = os.path.join(file_path,"Formula")
    Picture_path = os.path.join(file_path,'PDF_Images/{}'.format(PDF_name))
    Table_path = os.path.join(file_path,'Table')
    TableExcel_path = os.path.join(file_path,'TableJsonResult')
    Enhancement_path = os.path.join(file_path,'test.jpg')

    # 初始化，便于后续裁剪使用
    img = cv2.imread(img_path)
    img_w = image_size.get_w(img_path)
    img_h = image_size.get_h(img_path)
    pageContent = {}
    n = 0

    if os.stat(label_file_path).st_size == 0:
        return {}
    lines = sorted(open(label_file_path), key=lambda s: s.split(' ')[2])
    m = 0
    for line in lines:
        line_list = line.split(" ")
        label = float(line_list[0])
        x_center = float(line_list[1])* img_w
        y_center = float(line_list[2])* img_h
        width = float(line_list[3]) * img_w  # aa[3]图片width
        height = float(line_list[4]) * img_h  # aa[4]图片height

        # 裁剪的时候将水平坐标延长，保证不被截断
        lefttopx = 5
        lefttopy = int(y_center - height / 2.0)+1
        rightdownx = int(img_w) - 5
        rightdowny = int(y_center + height / 2.0)+1
        coor_list = '{},{},{},{}'.format(lefttopx, lefttopy, rightdownx, rightdowny)

        roi = img[lefttopy:rightdowny, lefttopx:rightdownx]
        #初始化easyocr
        reader = easyocr.Reader(
            ['ch_sim', 'en'],
            gpu=False,
            model_storage_directory='models',
            user_network_directory='models'
        )
        content = ''

        cv2.imwrite(crops_path, roi)
        Enhancement_Test.Enhancement(file_path)
        results = reader.readtext(Enhancement_path)
        # 提取文本内容，去除坐标和可信度参数
        for result in results:
            content += result[1]
        os.remove(crops_path)
        if len(content) == 0:
            continue
        try:
            with open(unit_change_path, "r", encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                keys = list(data.keys())
                for key in keys:
                    if key in content:
                        content.replace(key,data[key])
        except:
            print(None)

        if label == 0:
            pageContent["caption_" + str(m)] = content
            pageContent["caption_" + str(m) + "_coordinate"] = coor_list

        elif label == 1:
            pageContent["Footnote" + str(m)] = content
            pageContent["Footnote_" + str(m) + "_coordinate"] = coor_list

        elif label == 2:
            formula_path = os.path.join(Formula_path, label_file_name+"_formula_" + str(n) + '.jpg')
            cv2.imwrite(formula_path, roi)
            cv2.imwrite(crops_path, roi)  # 写入crops_path是为了方便接下来的识别
            # content = formulaTest.OCRAndFormulaProcess(crops_path)
            # if len(content)==0:
            #     continue
            os.remove(crops_path)
            pageContent["Formula" + str(n)] = "formula_content"
            pageContent["FormulaImage_path" + str(n)] = formula_path
            pageContent["Formula_" + str(n) + "_coordinate"] = coor_list
            n += 1
            pass

        elif label == 3:
            pageContent["Page-footer" + str(m)] = content
            pageContent["Page-footer_" + str(m) + "_coordinate"] = coor_list

        elif label == 4:
            pageContent["Page-header" + str(m)] = content
            pageContent["Page-header_" + str(m) + "_coordinate"] = coor_list

        elif label == 5:
            picture_path = os.path.join(Picture_path,PDF_name+str(m)+'.jpg')
            cv2.imwrite(picture_path, roi)
            pageContent["Picture" + str(m)] = picture_path
            pageContent["Picture_" + str(m) + "_coordinate"] = coor_list

        elif label == 6:
            pageContent["Section-header" + str(m)] = content
            pageContent["Section-header_" + str(m) + "_coordinate"] = coor_list

        elif label == 7:
            table_path = os.path.join(Table_path, PDF_name + str(m) + '.jpg')
            table_excel_path = os.path.join(TableExcel_path, PDF_name + str(m) + '.xlsx')
            if os.path.exists(table_excel_path) == False:
                open(table_excel_path,'w')
            TableProcess.tableProcess(PDF_path, int(page_num)-1, table_excel_path)
            cv2.imwrite(table_path, roi)
            pageContent["table_path" + str(m)] = table_path
            pageContent["table_excel_path" + str(m)] = table_excel_path
            pageContent["table_" + str(m) + "_coordinate"] = coor_list
            pass

        elif label == 8:
            pageContent["paragraph" + str(m)] = content
            pageContent["paragraph_" + str(m) + "_coordinate"] = coor_list

        elif label == 9:
            pageContent["Title" + str(m)] = content
            pageContent["Title_" + str(m) + "_coordinate"] = coor_list
        m += 1

    return pageContent