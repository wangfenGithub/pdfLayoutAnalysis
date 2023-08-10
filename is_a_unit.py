def isa_unit(first_content,second_content):
    first_content_section_name = first_content["section_name"]
    second_content_section_name = second_content["section_name"]

    len_1 = len(first_content_section_name)
    len_2 = len(second_content_section_name)
    first_position_0,second_position_0=0,-1
    first_position_2,second_position_2 = 0,-1
    first_position_4,second_position_4 = 0,-1
    first_position_6,second_position_6 = 0,-1
    #第一个section_name的前几位
    if len_1>0:
        first_position_0 = first_content_section_name[0]
    if len_1 > 2:
        first_position_2 = first_content_section_name[2]
    if len_1 > 4:
        first_position_4 = first_content_section_name[4]
    if len_1 > 6:
        first_position_6 = first_content_section_name[6]
    # 第二个section_name的前几位
    if len_2>0:
        second_position_0 = second_content_section_name[0]
    if len_2 > 2:
        second_position_2 = second_content_section_name[2]
    if len_2 > 4:
        second_position_4 = second_content_section_name[4]
    if len_2 > 6:
        second_position_6 = second_content_section_name[6]

    if len_1>2 and len_2>2 and first_position_0 == second_position_0 and first_position_2 != second_position_2:
        if first_position_2.isdigit() == False:
            #第一位数字相同，第二位数字不同，并且第一个单元格的第二位不是数字，则表明是嵌套关系
            return True
        else:
            return False
    if len_1>4 and len_2>4 and first_position_0 == second_position_0 and first_position_2 == second_position_2 and first_position_4 != second_position_4:
        if first_position_4.isdigit() == False:
            #第一位数字相同，第二位数字不同，并且第一个单元格的第二位不是数字，则表明是嵌套关系
            return True
        else:
            return False
    if len_1>6 and len_2>6 and first_position_0 == second_position_0 and first_position_2 == second_position_2 and first_position_4 == second_position_4 and first_position_6 != second_position_6:
        if first_position_6.isdigit() == False:
            #第一位数字相同，第二位数字不同，并且第一个单元格的第二位不是数字，则表明是嵌套关系
            return True
        else:
            return False

