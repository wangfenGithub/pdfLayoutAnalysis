def sort(dict_content):
    # 首先需要对pageContent页进行排序,按照page_1,page_2,page_3。。。的顺序
    dict_content_keys = list(dict_content.keys())
    dict_content_new = {}
    i = 0
    page_str = ""
    j = 0
    while i < len(dict_content_keys):
        dict_content_key = dict_content_keys[i]
        if i == 0:
            dict_content_new["filename"] = dict_content[dict_content_key]
            i += 1
            continue
        page_str = "page_" + str(j)
        if page_str in dict_content_keys:
            dict_content_new[page_str] = dict_content[page_str]
            i += 1
        j += 1

    return dict_content_new