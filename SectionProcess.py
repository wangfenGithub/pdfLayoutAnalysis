# encoding='utf-8'

def SectionProcess(pageContent,flag_time = 0):
    pageContent_new = {}

    keys_list = list(pageContent.keys())
    len_keys = len(keys_list)
    flag = 1  # 标志还没有遇到Section
    m = 1  # 标志第几个Section
    i = 0

    while i<len_keys:
        key_name = keys_list[i]
        # 如果内容为空则不处理
        if len(pageContent[key_name])==0:
            i += 2
            continue

        # 如果没遇到第一个Section那就一直加
        if ("Section" not in key_name) and flag:
            pageContent_new[key_name] = pageContent[key_name]
            i += 1
            continue

        # 遇到Section过后,做处理
        if "Section" in key_name:
            flag = 0 #标志已经遇到section了，以后的内容都是section中的
            section_content = {}

            section_content["section_name"] = pageContent[key_name]
            i += 1  # 加一是因为还有与之对应的坐标
            key_name = keys_list[i]
            section_content["section_name_coordinate"] = pageContent[key_name]

            i += 1
            j = i
            #len_keys-3是因为最后的page_footer单独处理
            while j >= i and j <= len_keys-3:
                key_name = keys_list[j]
                if len(pageContent[key_name]) == 0:#去除内容为空的字段
                    j+=2
                    continue

                if "Section" not in key_name:
                    # 如果在遇到一个section之后没有再遇到下一个section，则表明在下一个section之前的内容都属于现在的section
                    section_content[key_name] = pageContent[key_name]
                    j += 1
                    if j<len_keys:
                        key_name = keys_list[j]
                        section_content[key_name] = pageContent[key_name]
                        j += 1
                        key_name = keys_list[j]
                        if "_coordinate" in key_name and "Formula" in key_name or "table" in key_name:
                            section_content[key_name] = pageContent[key_name]
                            j += 1
                else:
                    # 在上一个section后又遇到了下一个section,则跳出本次循环
                    pageContent_new["first_level_section_"+str(m)] = section_content
                    m += 1
                    i = j
                    break
            # 如果是因为j==len_keys-2跳出循环的，那么最后一个section则需要单独处理，并且判断最后两个标签是否为页脚
            if j == len_keys:
                pageContent_new["first_level_section_" + str(m)] = section_content
                break
            if j == len_keys-2:
                key_name = keys_list[j]
                if "Section-header" not in key_name:
                    section_content[key_name] = pageContent[key_name]
                    j += 1
                    key_name = keys_list[j]
                    section_content[key_name] = pageContent[key_name]
                    #如果不是页脚，则继续写入section
                    if "Page-footer" not in key_name:
                        pageContent_new["first_level_section_"+str(m)] = section_content
                else:
                    pageContent_new["first_level_section_" + str(m)] = section_content
                    m += 1
                    section_content = {}
                    section_content["section_name"] = pageContent[key_name]
                    j += 1  # 加一是因为还有与之对应的坐标
                    key_name = keys_list[j]
                    section_content["section_name_coordinate"] = pageContent[key_name]
                    pageContent_new["first_level_section_" + str(m)] = section_content

                #如果不是页脚，则不需要写入section，直接写入pageContent_new就行
                i = len_keys

    # while i<len_keys:
    #     key_name = keys_list[i]
    #     # 如果内容为空则不处理
    #     if len(pageContent[key_name])==0:
    #         i += 2
    #         continue
    #
    #     # 如果没遇到第一个Section那就一直加
    #     if ("Section" not in key_name) and flag:
    #         pageContent_new[key_name] = pageContent[key_name]
    #         i += 1
    #         pass
    #
    #     # 遇到Section过后,做处理
    #     if "Section" in key_name:
    #         flag = 0
    #         section_content = {}
    #         first_position_char_F = pageContent[key_name][0]
    #
    #         section_content["section_name"] = pageContent[key_name]
    #         i += 1  # 加一是因为还有与之对应的坐标
    #         key_name = keys_list[i]
    #         section_content["section_name_coordinate"] = pageContent[key_name]
    #
    #         j = i + 1
    #         while j >= i + 1 and j < len_keys:
    #             key_name = keys_list[j]
    #             if "Section" in key_name:
    #                 if len(pageContent[key_name]) == 0:
    #                     j += 2
    #                     continue
    #                 first_position_char_C = pageContent[key_name][0]
    #                  #如果第一位数字不相等，说明一级标题第一个位上的数字不同，则
    #                 if flag_time == 1:
    #                     if first_position_char_C != first_position_char_F:
    #                         pageContent_new["section_" + str(m)] = section_content
    #                         m += 1
    #                         i = j
    #                         break
    #                     else:
    #                         # 如果第一个数字相同，则属于子标题，则先写道第一个标题里，下一次调用这个函数再处理
    #                         section_content[key_name] = pageContent[key_name]
    #                         j += 1
    #                         key_name=keys_list[j]
    #                         section_content[key_name] = pageContent[key_name]
    #             else:
    #                 section_content[key_name] = pageContent[key_name]
    #                 j += 1
    #                 if j<len_keys:
    #                     key_name = keys_list[j]
    #                     section_content[key_name] = pageContent[key_name]
    #             j += 1
    #         if j == len_keys or i == len_keys:
    #             i = j
    #             pageContent_new["section_"+str(m)] = section_content
    return pageContent_new

