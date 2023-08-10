# encoding='utf-8'
import json
import os

import KuaYeProcess
import SectionProcess
import SingleSideProcess
import SjQiantao
import SortPage
import is_a_unit

def PDFProcess(Predicted_Labels_path,file_path,unit_change_path):
    """
    :param Predicted_Labels_path: 标签文件存放文件夹，例如：“***\All_Label\Labels”
    :param file_path: 从yaml配置文件读取的本项目的根路径
    :param unit_change_path:单位配置文件路径
    :return:没有返回，因为调用的函数已经保存了对应的json
    """
    dirs = os.listdir(Predicted_Labels_path)
    for PDF_name in dirs:

        label_dir = os.path.join(Predicted_Labels_path, PDF_name)
        # 一个pdf对应的由yolov7预测的所有标签文件
        labels = os.listdir(label_dir)

        Img_root_path = os.path.join(file_path,'PDF_Images')
        image_dir_path = os.path.join(Img_root_path, PDF_name)

        json_str = Process(PDF_name, label_dir, image_dir_path, labels,file_path,unit_change_path)
        # return json_str


def Process(PDF_name,label_dir,Img_Dir_path,labels,file_path,unit_change_path):
    """
    :param PDF_name: 这是pdf去掉.pdf后缀后的文件名，也是标签文件夹名,例如：“File1”
    :param label_dir: 一个pdf对应的标签文件夹路径，例如：“***\All_Label\Labels\File1”
    :param Img_Dir_path: 一个pdf对应的图片文件夹路径，例如："***\PDF_Images\File1"
    :param labels: 一个pdf对应的由yolov7预测的所有txt标签文件
    :param file_path: 从配置文件读取的本项目的根路径
    :param unit_change_path 单位配置文件路径
    :return:
    """
    old_File_name = ''
    dict_content = {}
    json_path = ''
    for file in labels:

        page_num = file.split(".")[0].split("_")[1]
        # 标签文件的路径,例如：D:\pythonProject\yolov7Process\All_Label\dizhi\File1_1.txt
        label_file_path = os.path.join(label_dir, file)
        # 获取标签文件名字，如果名字改变，则重新构建json文件，例如：File1_1
        label_file_name = file.split(".")[0]

        #获取对应的pdf文件名，便于表格做处理
        PDF_dir = os.path.join(file_path,'PDF')
        PDF_path = os.path.join(PDF_dir,PDF_name+".pdf")

        if PDF_name != old_File_name:
            dict_content = {}
            # 获取该标签文件所对应的图片所在路径
            img_path = os.path.join(Img_Dir_path, label_file_name + '.jpg')
            JSON_save_path = os.path.join(file_path,'JSON_New')
            # 那说明是PDF文件的第一页，则单独处理,并新建json文件
            json_path = os.path.join(JSON_save_path, PDF_name + ".json")
            if os.path.exists(json_path):
                os.remove(json_path)
            if not os.path.exists(json_path):
                open(json_path,'w')

            dict_content["filename"] = PDF_name
            result1 = SingleSideProcess.SingleSidePageProcess(label_file_path,label_file_name,img_path,PDF_name,page_num,PDF_path,file_path,unit_change_path)
            if result1:
                dict_content["page_" +page_num] = result1
        else:
            # 获取该标签文件所对应的图片
            img_path = os.path.join(Img_Dir_path, label_file_name + '.jpg')
            result2 = SingleSideProcess.SingleSidePageProcess(label_file_path,label_file_name,img_path,PDF_name,page_num,PDF_path,file_path,unit_change_path)
            if result2:
                dict_content["page_"+page_num] = result2

        # 标记处理过的文件名
        old_File_name = PDF_name

    print("一个文档的内容dict_content:")
    print(dict_content)

    # 对页面page进行排序
    dict_content_new = SortPage.sort(dict_content)

    #排序完成，然后进行跨页处理
    dict_content_new_2 = KuaYeProcess.KuaYeProcess(dict_content_new)

    #获取dict_content_new_2的所有keys，处理一级嵌套关系
    pages = list(dict_content_new_2.keys())
    dict_content_new_3 = {}
    i = 0
    while i<len(pages):
        page = pages[i]
        if i==0:
            dict_content_new_3[page] = dict_content_new_2[page]
            i += 1
            continue
    #    获取一整页的内容
        pageContent = {}
        pageContent = dict_content_new_2[page]
        flag_time = 0
        pageContent_new = SectionProcess.SectionProcess(pageContent,flag_time)#处理一级标题嵌套

        pageContent_new_1 = {}
        # 处理二级标题嵌套
        pageContent_keys = list(pageContent_new.keys())
        j = 0
        num = 0
        while j<len(pageContent_keys):
            key_1 = pageContent_keys[j]
            if "section" in key_1:
                #第一个单元的所有值（字典形式）
                first_content = pageContent_new[key_1]
                j = j+1
                while j<len(pageContent_keys):
                    key_2 = pageContent_keys[j]
                    if "section" not in key_2:
                        break
                    #下一个单元的所有值（字典形式）
                    second_content = pageContent_new[key_2]
                    #如果遇到section不为数字，则直接将其并入其中
                    if second_content["section_name"][0].isdigit()==False:
                        first_content["second_level_section_child_" + str(num)] = second_content
                        del pageContent_new[key_2]
                        j += 1
                        num += 1
                        continue

                    #判断是否为嵌套关系
                    is_unit = is_a_unit.isa_unit(first_content,second_content)
                    if is_unit:
                        first_content["second_level_section_child_"+str(num)] = second_content
                        del pageContent_new[key_2]
                        j += 1
                        num += 1
                    else:
                        j -= 1
                        break
                pageContent_new_1[key_1] = first_content
            else:
                pageContent_new_1[key_1] = pageContent_new[key_1]
            j += 1

        #处理三级嵌套关系
        pageContent_3 = SjQiantao.SjQiantao(pageContent_new_1)
        dict_content_new_3[page] = pageContent_new_1
        i += 1

    json_str = json.dumps(dict_content_new_3, indent=4, ensure_ascii=False)
    with open(json_path, 'w') as json_file:
        json_file.write(json_str)

    return json_str

