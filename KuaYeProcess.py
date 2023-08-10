# encoding='utf-8'
def KuaYeProcess(dict_content_new):
    pageContent_KuaYe = {}
    pages = list(dict_content_new)
    pages_len = len(pages)
    #遍历
    i = 0
    while i<pages_len:
        now_page_name = pages[i]
        if i == 0 or i==1:
            pageContent_KuaYe[now_page_name] = dict_content_new[now_page_name]
            i += 1
            continue
            #从第二页开始单独处理
            #获取上一页面的key，例如现在处理page_2，上一页面为page_1
        last_page_name = pages[i-1]
        #获取目前这个section中的内容，从而获取section_name,加到下一页中
        last_page_keys = list(dict_content_new[last_page_name].keys())
        #初始化section列表
        last_sections = []
        for key in last_page_keys:
            if "Section" in key:
                last_sections.append(key)
                pass
        now_page_keys = list(dict_content_new[now_page_name].keys())
        page_content_new = {}
        L = len(last_sections)
        if L>0 and len(now_page_keys)>2:
            # 上一页最后一个section的key
            key = last_sections[L - 2]
            coordi = last_sections[L - 1]
            #若下一页存在页眉，则判断在页眉和第一个section之间是否存在其他内容，若存在，则把上一页最后一个section加到下一页中
            if "Page-header" in now_page_keys[0] and "Section-header" not in now_page_keys[2]:
                #上一页中如果存在section,则先拿到最后一个section以及最后一个section对应的坐标
                page_content_new["Page-header"] = dict_content_new[now_page_name]["Page-header0"]
                page_content_new["Page-header_coordinate"] = dict_content_new[now_page_name]["Page-header_0_coordinate"]
                page_content_new["Section-header_last"] = dict_content_new[last_page_name][key]
                page_content_new["Section-header_last_coordinate"] = dict_content_new[last_page_name][coordi]
            elif "Page-header" not in now_page_keys[0] and "Section-header" not in now_page_keys[0]:
                page_content_new["Section-header_last"] = dict_content_new[last_page_name][key]
                page_content_new["Section-header_last_coordinate"] = dict_content_new[last_page_name][coordi]

        #然后再把现在这个section中的内容追加到page_content_new中
        for key in now_page_keys:
            if "Page-header" in key:
                continue
            page_content_new[key] = dict_content_new[now_page_name][key]
        pageContent_KuaYe[now_page_name] = page_content_new
        i += 1

    return pageContent_KuaYe

    # pageContent_KuaYe = {}
    # pages = list(pageContent.keys())
    # key_len = len(pages)
    # i = 0
    # while i<key_len:
    #     page_content_new = {}
    #     last_sections = []
    #     now_page_name = pages[i]
    #     if i == 0 or i==1:
    #         pageContent_KuaYe[now_page_name] = pageContent[now_page_name]
    #         i += 1
    #         continue
    #
    #     last_page_name = pages[i - 1]
    #     # pageContent_KuaYe[key_name] = pageContent[key_name]
    #     #获取目前这个section中的内容，从而获取section_name,加到下一页中
    #     last_page_keys = list(pageContent[last_page_name].keys())
    #     for key in last_page_keys:
    #         if "Section" in key:
    #             last_sections.append(key)
    #             pass
    #     now_page_keys = list(pageContent[now_page_name].keys())
    #
    #     L = len(last_sections)
    #     if L>1:
    #         if ("Page-header" in now_page_keys[0] and "Section-header" not in now_page_keys[2]) or ("Page-header" not in now_page_keys[0] and "Section-header" in now_page_keys[0]):
    #             #上一页中如果存在section,则先拿到最后一个section以及最后一个section对应的坐标
    #             #上一页section的key
    #             key = last_sections[L-2]
    #             coordi = last_sections[L-1]
    #             page_content_new["Section-header_last"] = pageContent[last_page_name][key]
    #             page_content_new["Section-header_last_coordinate"] = pageContent[last_page_name][coordi]
    #
    #     #然后再把现在这个section中的内容追加到page_content_new中
    #     for key in now_page_keys:
    #         page_content_new[key] = pageContent[now_page_name][key]
    #     pageContent_KuaYe[now_page_name] = page_content_new
    #     i += 1
    #
    # return pageContent_KuaYe



