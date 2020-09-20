import re
from LAC import LAC
from extract.resume import *
from extract.internship import split_by_time, has_time, is_company, is_position, preprocess

"""
重点规则是职务 学生职务相对有限，但目前收录较少，规则仍需完善
"""

cps_pattern_time = re.compile(r'\d{4}\.(\d+)? *[-~至]?')
cps_pattern_org = re.compile(r'[ \t]*(.*(协会)|(社团)|(团队)|(学生会)|(学院))[ \t]*$')
cps_pattern_pos = re.compile(r'(.*([会部班]长)|([组队成委]员)|(负责人)|(编辑)|(支书)|(学委)|(主席)|(干事)|(者)|(大使))')


def cps_time_pos_depict(exp_string):
    """
    获取校园经历的时间、岗位、描述

    :param exp_string: 经历字符串
    :return: 提取的对应信息的列表，每个列表是一个三元组
    """
    exp_list = split_by_time(exp_string, cps_pattern_time, cps_pattern_org, cps_pattern_pos)
    extract_list = []
    # 时间、岗位、描述的提取，这里只考虑了三者全在一行、时间一行剩下的两个一行两种情况
    for exp in exp_list:
        # print(exp)
        first = exp[0]
        first_list = preprocess(first)
        # print(first_list)
        time = None
        org = None
        pos = None
        depict = None
        other = []
        # 一行包括多个信息的情况
        if len(first_list) >= 2:
            for idx, item in enumerate(first_list):
                # print(item)
                if has_time(item, cps_pattern_time) and time is None:
                    time = item
                elif is_position(item, cps_pattern_pos) and pos is None:
                    pos = item
                else:
                    other.append(item)
            if len(other):
                depict = '\n'.join(other) + '\n'.join(exp[1:])
            else:
                depict = '\n'.join(exp[1:])
            # print([time, org, pos], '\n', depict)
        # 一行只有一个信息的情况
        elif len(first_list) == 1:
            if has_time(first_list[0], cps_pattern_time):
                time = first_list[0]
            # 继续提取org、pos
            if len(exp) > 1:
                second = exp[1]
                second_list = preprocess(second)
                # print(second_list)
                for idx, item in enumerate(second_list):
                    if is_position(item, cps_pattern_pos) and pos is None:
                        pos = item
                    else:
                        other.append(item)
            if len(exp) > 2:
                if len(other):
                    depict = '\n'.join(other) + '\n'.join(exp[2:])
                else:
                    depict = '\n'.join(exp[2:])
            # print([time, org, pos], '\n', depict)
        if sum([x is not None for x in [time, org, pos, depict]]) >= 2:
            extract_list.append((time, pos, depict))
    for item in extract_list:
        print(item)
    # print(extract_list, '\n', len(extract_list))
    print(len(extract_list))
    return extract_list


def test():
    for cps_string in campus_string_list:
        cps_time_pos_depict(cps_string)


if __name__ == '__main__':
    test()

