# encoding='utf-8'

def SectionProcess(pageContent,flag_time = 0):
    pageContent_new = {}

    keys_list = list(pageContent.keys())
    len_keys = len(keys_list)
    flag = 1  # ��־��û������Section
    m = 1  # ��־�ڼ���Section
    i = 0

    while i<len_keys:
        key_name = keys_list[i]
        # �������Ϊ���򲻴���
        if len(pageContent[key_name])==0:
            i += 2
            continue

        # ���û������һ��Section�Ǿ�һֱ��
        if ("Section" not in key_name) and flag:
            pageContent_new[key_name] = pageContent[key_name]
            i += 1
            continue

        # ����Section����,������
        if "Section" in key_name:
            flag = 0 #��־�Ѿ�����section�ˣ��Ժ�����ݶ���section�е�
            section_content = {}

            section_content["section_name"] = pageContent[key_name]
            i += 1  # ��һ����Ϊ������֮��Ӧ������
            key_name = keys_list[i]
            section_content["section_name_coordinate"] = pageContent[key_name]

            i += 1
            j = i
            #len_keys-3����Ϊ����page_footer��������
            while j >= i and j <= len_keys-3:
                key_name = keys_list[j]
                if len(pageContent[key_name]) == 0:#ȥ������Ϊ�յ��ֶ�
                    j+=2
                    continue

                if "Section" not in key_name:
                    # ���������һ��section֮��û����������һ��section�����������һ��section֮ǰ�����ݶ��������ڵ�section
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
                    # ����һ��section������������һ��section,����������ѭ��
                    pageContent_new["first_level_section_"+str(m)] = section_content
                    m += 1
                    i = j
                    break
            # �������Ϊj==len_keys-2����ѭ���ģ���ô���һ��section����Ҫ�������������ж����������ǩ�Ƿ�Ϊҳ��
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
                    #�������ҳ�ţ������д��section
                    if "Page-footer" not in key_name:
                        pageContent_new["first_level_section_"+str(m)] = section_content
                else:
                    pageContent_new["first_level_section_" + str(m)] = section_content
                    m += 1
                    section_content = {}
                    section_content["section_name"] = pageContent[key_name]
                    j += 1  # ��һ����Ϊ������֮��Ӧ������
                    key_name = keys_list[j]
                    section_content["section_name_coordinate"] = pageContent[key_name]
                    pageContent_new["first_level_section_" + str(m)] = section_content

                #�������ҳ�ţ�����Ҫд��section��ֱ��д��pageContent_new����
                i = len_keys

    # while i<len_keys:
    #     key_name = keys_list[i]
    #     # �������Ϊ���򲻴���
    #     if len(pageContent[key_name])==0:
    #         i += 2
    #         continue
    #
    #     # ���û������һ��Section�Ǿ�һֱ��
    #     if ("Section" not in key_name) and flag:
    #         pageContent_new[key_name] = pageContent[key_name]
    #         i += 1
    #         pass
    #
    #     # ����Section����,������
    #     if "Section" in key_name:
    #         flag = 0
    #         section_content = {}
    #         first_position_char_F = pageContent[key_name][0]
    #
    #         section_content["section_name"] = pageContent[key_name]
    #         i += 1  # ��һ����Ϊ������֮��Ӧ������
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
    #                  #�����һλ���ֲ���ȣ�˵��һ�������һ��λ�ϵ����ֲ�ͬ����
    #                 if flag_time == 1:
    #                     if first_position_char_C != first_position_char_F:
    #                         pageContent_new["section_" + str(m)] = section_content
    #                         m += 1
    #                         i = j
    #                         break
    #                     else:
    #                         # �����һ��������ͬ���������ӱ��⣬����д����һ���������һ�ε�����������ٴ���
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

