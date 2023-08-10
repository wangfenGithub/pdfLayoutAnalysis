import is_a_unit


def SjQiantao(pageContent_new):
    pageContent_3 = {}
    pageContent_keys = list(pageContent_new.keys())
    j = 0
    num = 0
    while j < len(pageContent_keys):
        key_1 = pageContent_keys[j]
        if "section" in key_1:
            # 第一个单元的所有值（字典形式）
            content = pageContent_new[key_1]
            # 拿到section中的所有keys,就可以对其中的section_child进行嵌套判断
            content_keys = list(content.keys())
            k = 0
            while k<len(content_keys):
                first_key = content_keys[k]
                if "section_child" in first_key:
                    first_child_content = pageContent_new[key_1][first_key]
                    k = k+1
                    while k < len(content_keys):
                        second_key = content_keys[k]
                        if "section_child" not in second_key:
                            break
                        # 下一个单元的所有值（字典形式）
                        second_child_content = pageContent_new[key_1][second_key]
                        if second_child_content["section_name"][0].isdigit() == False:
                            first_child_content["third_level_section_child_" + str(num)] = second_child_content
                            del pageContent_new[key_1][second_key]
                            k += 1
                            num += 1
                            continue
                        # 判断是否为嵌套关系
                        is_unit = is_a_unit.isa_unit(first_child_content, second_child_content)
                        if is_unit:
                            first_child_content["third_level_section_child_" + str(num)] = second_child_content
                            del pageContent_new[key_1][second_key]
                            k += 1
                            num += 1
                        else:
                            k -= 1
                            break
                    pageContent_3[key_1] = first_child_content
                else:
                    pageContent_3[key_1] = pageContent_new[key_1][first_key]
                k += 1
        j += 1
    return pageContent_3
