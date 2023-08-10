import json
import os.path
import cv2
import yaml
import image_size


def extract_image(config_file_path):
    try:
        with open(config_file_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            file_path = data['path']
            All_Labels_dir = os.path.join(file_path,'All_Label/Labels')
            PDF_Images_dir = os.path.join(file_path,'PDF_Images')
            Cut_Images_dir = os.path.join(file_path, 'Images')
            Cut_Image_Json_dir = os.path.join(file_path,'ImagesJsonResult')
            pageContent = {}
            All_Labels_dirs = os.listdir(All_Labels_dir)
            for PDF_name in All_Labels_dirs:
                Label_dir = os.path.join(All_Labels_dir,PDF_name)
                Image_dir = os.path.join(PDF_Images_dir,PDF_name)
                Cut_Images_PDF_Name_Dir = os.path.join(Cut_Images_dir,PDF_name)
                json_path = os.path.join(Cut_Image_Json_dir,"{}.json".format(PDF_name))

                if os.path.exists(Cut_Images_PDF_Name_Dir) == False:
                    os.mkdir(Cut_Images_PDF_Name_Dir)

                labels = os.listdir(Label_dir)
                m = 0
                for label in labels:
                    label_name = label.split(".")[0]
                    label_file_path = os.path.join(Label_dir,label)
                    #完整图片的路径
                    image_file_path = os.path.join(Image_dir,label_name+'.jpg')
                    with open(label_file_path,"r",encoding="utf-8") as f2:
                        lines = f2.readlines()
                        for line in lines:
                            line_list = line.split(" ")
                            label = float(line_list[0])
                            if int(label) != 6:
                                continue
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

                            cut_image_path = os.path.join(Cut_Images_PDF_Name_Dir, PDF_name +"_"+ str(m) + '.jpg')
                            if os.path.exists(cut_image_path) == False:
                                open(cut_image_path, 'w')
                            cv2.imwrite(cut_image_path, roi)
                            pageContent["Picture_" + str(m)] = cut_image_path
                            pageContent["Picture_" + str(m) + "_coordinate"] = coor_list
                            m += 1
    except:
        print(None)

    json_str = json.dumps(pageContent, indent=4, ensure_ascii=False)
    with open(json_path, 'w') as json_file:
        json_file.write(json_str)

