import json
import os.path

import cv2
import yaml

import TableProcess
import image_size


def extract_table(config_file_path):
    try:
        with open(config_file_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            file_path = data['path']
            All_Labels_dir = os.path.join(file_path,'All_Label/Labels')
            PDF_Images_dir = os.path.join(file_path,'PDF_Images')
            Table_dir = os.path.join(file_path, 'Table')
            TableExcel_path = os.path.join(file_path, 'TableExcelResult')
            PDF_dir = os.path.join(file_path,'PDF')
            Table_Json_dir = os.path.join(file_path,'TableJsonResult')
            pageContent = {}
            All_Labels_dirs = os.listdir(All_Labels_dir)
            for PDF_name in All_Labels_dirs:
                print("pdf_name:{}".format(PDF_name))
                Label_dir = os.path.join(All_Labels_dir,PDF_name)
                Image_dir = os.path.join(PDF_Images_dir,PDF_name)
                PDF_path = os.path.join(PDF_dir,PDF_name+'.pdf')
                Table_path = os.path.join(Table_dir, PDF_name)
                json_path = os.path.join(Table_Json_dir,"{}.json".format(PDF_name))
                if os.path.exists(Table_path) == False:
                    os.mkdir(Table_path)
                labels = os.listdir(Label_dir)
                m = 0
                for label in labels:
                    label_name = label.split(".")[0]
                    page_num = label.split(".")[0].split("_")[1]
                    label_file_path = os.path.join(Label_dir,label)
                    image_file_path = os.path.join(Image_dir,label_name+'.jpg')
                    with open(label_file_path,"r",encoding="utf-8") as f2:
                        lines = f2.readlines()
                        for line in lines:
                            line_list = line.split(" ")
                            label = float(line_list[0])

                            if int(label) != 7:
                                continue
                            print("label={}".format(label))
                            img = cv2.imread(image_file_path)
                            img_w = image_size.get_w(image_file_path)
                            img_h = image_size.get_h(image_file_path)

                            x_center = float(line_list[1]) * img_w
                            y_center = float(line_list[2]) * img_h
                            width = float(line_list[3]) * img_w  # aa[3]图片width
                            height = float(line_list[4]) * img_h  # aa[4]图片height

                            # 裁剪的时候将水平坐标延长，保证不被截断
                            lefttopx = 5
                            lefttopy = int(y_center - height / 2.0) + 1
                            rightdownx = int(img_w) - 5
                            rightdowny = int(y_center + height / 2.0) + 1
                            coor_list = '{},{},{},{}'.format(lefttopx, lefttopy, rightdownx, rightdowny)

                            roi = img[lefttopy:rightdowny, lefttopx:rightdownx]

                            table_path = os.path.join(Table_path, PDF_name + str(m) + '.jpg')
                            table_excel_path = os.path.join(TableExcel_path, PDF_name + str(m) + '.xlsx')
                            if os.path.exists(table_excel_path) == False:
                                open(table_excel_path, 'w')
                            TableProcess.tableProcess(PDF_path, int(page_num) - 1, table_excel_path)
                            cv2.imwrite(table_path, roi)
                            pageContent["table_path" + str(m)] = table_path
                            pageContent["table_excel_path" + str(m)] = table_excel_path
                            pageContent["table_" + str(m) + "_coordinate"] = coor_list
                            m += 1
    except:
        print(None)

    json_str = json.dumps(pageContent, indent=4, ensure_ascii=False)
    with open(json_path, 'w') as json_file:
        json_file.write(json_str)

if __name__ == '__main__':
    config_file_path = r"D:\codeMyself\pythonProject\KUNLun_Bushu\peizhi.yaml"
    extract_table(config_file_path)