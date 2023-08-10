import os

from PIL import Image
# from pytesseract import pytesseract
import easyocr
import SectionProcess
import image_size
import cv2
import Enhancement_Test
import TableProcess
# import formulaTest

crops_path = r".\crops\temp.jpg"
Formula_path = r'.\Formula'
Picture_path = r'.\Picture'
Table_path = r'.\Table'
TableExcel_path = r'.\TableJsonResult'
Enhancement_path = r".\test.jpg"

def SingleSidePageProcess(label_file_path,label_file_name,img_path,file_name,page_num,PDF_path):
    # 初始化，便于后续裁剪使用
    img = cv2.imread(img_path)
    img_w = image_size.get_w(img_path)
    img_h = image_size.get_h(img_path)
    pageContent = {}
    pageContent_new = {}
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

        lefttopx = int(x_center - width / 2.0)
        lefttopy = int(y_center - height / 2.0)
        if int(x_center + width / 2.0)+40<width:
            rightdownx = int(x_center + width / 2.0) + 40
        elif int(x_center + width / 2.0)+30<width:
            rightdownx = int(x_center + width / 2.0) + 30
        elif int(x_center + width / 2.0)+20<width:
            rightdownx = int(x_center + width / 2.0) + 20
        elif int(x_center + width / 2.0)+10<width:
            rightdownx = int(x_center + width / 2.0) + 10
        else:
            rightdownx = int(x_center + width / 2.0)

        if int(y_center + height / 2.0)+40<height:
            rightdowny = int(y_center + height / 2.0) + 40
        elif int(y_center + height / 2.0)+30<height:
            rightdowny = int(y_center + height / 2.0) + 30
        elif int(y_center + height / 2.0)+20<height:
            rightdowny = int(y_center + height / 2.0) + 20
        elif int(y_center + height / 2.0)+10<height:
            rightdowny = int(y_center + height / 2.0) + 10
        else:
            rightdowny = int(y_center + height / 2.0)




        coor_list = '{},{},{},{}'.format(lefttopx, lefttopy, rightdownx, rightdowny)
        #裁剪的时候将水平坐标延长，保证不被截断
        lefttopx = 15
        rightdownx = rightdownx + 10
        if rightdownx<width/2.0:
            rightdownx = int(width/2.0)
        else:
            rightdownx = int(width)
        roi = img[lefttopy:rightdowny, lefttopx:rightdownx]
        #初始化
        reader = easyocr.Reader(
            ['ch_sim', 'en'],
            gpu=False,
            model_storage_directory='models',
            user_network_directory='models'
        )
        content = ''
        if label == 0:
            cv2.imwrite(crops_path, roi)
            Enhancement_Test.Enhancement()
            results = reader.readtext(Enhancement_path)
            # 提取文本内容，去除坐标和可信度参数
            for result in results:
                content += result[1]
            os.remove(crops_path)
            if len(content)==0:
                continue
            pageContent["caption_" + str(m)] = content
            pageContent["caption_" + str(m) + "_coordinate"] = coor_list
        elif label == 1:
            cv2.imwrite(crops_path, roi)
            Enhancement_Test.Enhancement()
            results = reader.readtext(Enhancement_path)
            # 提取文本内容，去除坐标和可信度参数
            for result in results:
                content += result[1]
            os.remove(crops_path)
            if len(content) == 0:
                continue
            pageContent["Footnote" + str(m)] = content
            pageContent["Footnote_" + str(m) + "_coordinate"] = coor_list
        elif label == 2:
            # formula_path = os.path.join(Formula_path, label_file_name+"_formula_" + str(n) + '.jpg')
            # cv2.imwrite(formula_path, roi)
            # cv2.imwrite(crops_path, roi)  # 写入crops_path是为了方便接下来的识别
            # content = formulaTest.OCRAndFormulaProcess(crops_path)
            #
            # if len(content)==0:
            #     continue
            # os.remove(crops_path)
            # pageContent["Formula" + str(n)] = content
            # pageContent["FormulaImage_path" + str(n)] = formula_path
            # pageContent["Formula_" + str(n) + "_coordinate"] = coor_list
            # n += 1
            pass
        elif label == 3:
            cv2.imwrite(crops_path, roi)
            Enhancement_Test.Enhancement()
            results = reader.readtext(Enhancement_path)
            # 提取文本内容，去除坐标和可信度参数
            for result in results:
                content += result[1]
            os.remove(crops_path)
            if len(content) == 0:
                continue
            os.remove(Enhancement_path)
            pageContent["List-item" + str(m)] = content
            pageContent["List-item_" + str(m) + "_coordinate"] = coor_list
        elif label == 4:
            cv2.imwrite(crops_path, roi)
            Enhancement_Test.Enhancement()
            results = reader.readtext(Enhancement_path)
            # 提取文本内容，去除坐标和可信度参数
            for result in results:
                content += result[1]
            os.remove(crops_path)
            if len(content) == 0:
                continue
            os.remove(Enhancement_path)
            pageContent["Page-footer" + str(m)] = content
            pageContent["Page-footer_" + str(m) + "_coordinate"] = coor_list
        elif label == 5:
            cv2.imwrite(crops_path, roi)
            Enhancement_Test.Enhancement()
            results = reader.readtext(Enhancement_path)
            # 提取文本内容，去除坐标和可信度参数
            for result in results:
                content += result[1]
            os.remove(crops_path)
            if len(content) == 0:
                continue
            os.remove(Enhancement_path)
            pageContent["Page-header" + str(m)] = content
            pageContent["Page-header_" + str(m) + "_coordinate"] = coor_list
        elif label == 6:
            picture_path = os.path.join(Picture_path,file_name+str(m)+'.jpg')
            cv2.imwrite(picture_path, roi)
            pageContent["Picture" + str(m)] = picture_path
            pageContent["Picture_" + str(m) + "_coordinate"] = coor_list
        elif label == 7:
            cv2.imwrite(crops_path, roi)
            Enhancement_Test.Enhancement()
            results = reader.readtext(Enhancement_path)
            # 提取文本内容，去除坐标和可信度参数
            for result in results:
                content += result[1]
            os.remove(crops_path)
            if len(content) == 0:
                continue
            os.remove(Enhancement_path)
            pageContent["Section-header" + str(m)] = content
            pageContent["Section-header_" + str(m) + "_coordinate"] = coor_list
        elif label == 8:
            # table_path = os.path.join(Table_path, file_name + str(m) + '.jpg')
            # table_excel_path = os.path.join(TableExcel_path, file_name + str(m) + '.xlsx')
            # if os.path.exists(table_excel_path) == False:
            #     open(table_excel_path,'w')
            # TableProcess.tableProcess(PDF_path, int(page_num)-1, table_excel_path)
            # cv2.imwrite(table_path, roi)
            # pageContent["table_path" + str(m)] = table_path
            # pageContent["table_excel_path" + str(m)] = table_excel_path
            # pageContent["table_" + str(m) + "_coordinate"] = coor_list
            pass
        elif label == 9:
            cv2.imwrite(crops_path, roi)
            Enhancement_Test.Enhancement()
            results = reader.readtext(Enhancement_path)
            # 提取文本内容，去除坐标和可信度参数
            for result in results:
                content += result[1]
            os.remove(crops_path)
            if len(content) == 0:
                continue
            pageContent["paragraph" + str(m)] = content
            pageContent["paragraph_" + str(m) + "_coordinate"] = coor_list
        elif label == 10:
            cv2.imwrite(crops_path, roi)
            Enhancement_Test.Enhancement()
            results = reader.readtext(Enhancement_path)
            # 提取文本内容，去除坐标和可信度参数
            for result in results:
                content += result[1]
            os.remove(crops_path)
            if len(content) == 0:
                continue
            os.remove(Enhancement_path)
            pageContent["Title" + str(m)] = content
            pageContent["Title_" + str(m) + "_coordinate"] = coor_list
        m += 1

    return pageContent