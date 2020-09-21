import re
import difflib
from LAC import LAC
from extract.resume import *

"""
观察发现主要规律  1. 基本上每段以带时间的行开头；2. 时间公司职务集中于前两段； 

规则  其中公司规则和职位规则不够完善
时间格式    r'\d{4}\.(\d+)? *[-~至]?'  只能识别中间带点的时间格式
公司规则    lac + r'[ \t]*(.*([所行报局室科社])|(公司))[ \t]*'
职位规则    r'(([柜专务队组成试术验究人导]员)|(实习生)|(负责人)|([助经管]理)|([护配产技造型验查作]工)|([医商容讲技估教程][师授])|([记愿]者)|(编辑))[ \t]*$'

去题头(已弃用，换用后续处理方式）    r'^[\s ]*^[\s ]*((工作)|(实习)|(项目)|(校外)|(实践))?((经[历验])|(实践)|(实习)|(活动)|(工作))[ \t]*\n'
公司机构的识别可以使用HanLP（基于bert，识别最好，较慢），其次stanza和lac

进一步想法：如果要求每个信息尽可能不为空，提取更加全面，可以对提取到的信息进行二次加工提取，譬如时间为空，可以在二级提取中更换时间模式，进行匹配

"""

itn_pattern_pos = re.compile(
    r'(([柜专务队组成试术验究人导文]员)|(实习生)|(负责人)|([助经管]理)|([护配产技造型验查作]工)|([医商容讲技估教程][师授])|([记愿]者)|(编辑))[ \t]*$')
itn_pattern_org = re.compile(r'[ \t]*(.*([所行报局室科社])|(公司))[ \t]*')
itn_pattern_time = re.compile(r'\d{4}\.(\d+)? *[-~至]?')


def has_time(string, pattern):
    """
    识别字符串中是否含有时间，问题是如果描述中出现类似格式的时间也会匹配上

    :param pattern: 自定义时间模式
    :param string: 待判断字符串
    :return: 含有时间返回true
    """
    # 与下面的模式相比可以识别不带点的时间格式，但不利于后续处理
    # pattern = re.compile(r'\d{4}[\.-](\d+)? *[-~至]?')
    if re.search(pattern, string) is not None:
        return True


def sim_rate(s, t, threshold=0.7):
    """
    比较s和t两字符串的差异，当相似度大于阈值threshold时返回true

    :param threshold: 阈值
    :param s: 第一个字符串
    :param t: 第二个字符串
    :return: 相似度大于阈值返回true
    """
    if difflib.SequenceMatcher(None, s, t).quick_ratio() >= threshold:
        return True
    else:
        return False


def is_position(string, pattern, extend=False):
    """
    判断字符串是否是职务，如果扩展标志extend为true则在不匹配规则时还会进行查表操作

    :param pattern: 自定义职位模式串
    :param string: 待判断是否为职务的字符串
    :param extend: 扩展标志，为True时遍历匹配职务表
    :return: 是职务返回True
    """
    if re.search(pattern, string) is not None:
        return True
    else:
        if extend:
            with open("./positions", 'r') as f:
                postr = f.read()
                pos_list = postr.split('\n')
                for pos in pos_list:
                    if sim_rate(pos, string):
                        return True
        return False


def is_company(string, pattern, extend=False):
    """
    判断字符串是否是公司,使用lac识别,使用自定义规则二次识别未被识别的，extend为True表示进行查表操作

    :param pattern: 自定义机构模式
    :param string: 待判断字符串
    :param extend: 是否查表
    :return: 是公司名称返回True
    """
    lac = LAC(mode='lac')
    res = lac.run(string)
    # print(res)
    labels = res[1]
    for lbl in labels:
        if lbl == 'ORG' or lbl == 'LOC':
            return True
    if re.search(pattern, string) is not None:
        return True
    if extend:
        # 目前corporations里面保存的为公司名称简写，若更换为全称则可能要更改规则
        with open("./corporations", 'r') as f:
            companies = f.read().split('\n')
            for company in companies:
                if string.find(company) != -1:
                    return True
    return False


def split_by_time(exp_string, pattern_time, pattern_org, pattern_pos):
    """
    根据时间格式将经历切分成一个个时间段的经历，返回经历列表

    :param pattern_pos: 自定义职位模式
    :param pattern_org: 自定义机构模式
    :param pattern_time: 自定义时间模式
    :param exp_string: 整个实习经历的字符串
    :return: 以时间为分割的经历列表
    """
    def has_org_pos(string):
        if is_company(string, pattern_org) and is_position(string, pattern_pos):
            return True
        else:
            return False

    # 去空行
    exp_string = re.sub(r'[ \t]*\n', '#####', exp_string)
    exp_string = re.sub(r'#{5,}', '\n', exp_string)
    string_list = exp_string.split('\n')
    idxs = []
    time_list = []
    # 根据时间切块，得到经历列表,对于没有时间的行须同时有公司和职务
    for idx, string in enumerate(string_list):
        if re.search(pattern_time, string) is not None or has_org_pos(string):
            idxs.append(idx)
            time_list.append(string)
    exp_list = []
    pre = idxs[0]
    for post in idxs[1:]:
        exp = string_list[pre:post]
        if len(exp):
            exp_list.append(exp)
        pre = post
    if len(string_list[pre:]):
        exp_list.append(string_list[pre:])
    # print(exp_list)
    return exp_list


def preprocess(string):
    # 消除：旁边的空格、句首指标项目符等等
    string = re.sub(r' *[:：] *', '：', string)
    string = re.sub(r'^[ \t]+', '', string)
    string = re.sub(r'^[ \t]*[•⚫«-][ \t]*', '', string)
    string = re.sub(r'[•⚫«”“]', '', string)
    string = re.sub(r'[ \t]*[~至-]+[ \t]*', '-', string)
    return re.split(r'(?:[ \t]+)', string)


def itn_time_com_pos_desp(exp_string):
    """
    获取每段经历的时间、公司、岗位、描述，返回经历的列表，每个经历是一个字典

    :param exp_string: 校外经历字符串
    :return: 每个字典包含四项time, com, pos, desp
    """
    exp_list = split_by_time(exp_string, itn_pattern_time, itn_pattern_org, itn_pattern_pos)
    extract_list = []
    # 时间、公司、职务、描述的提取，这里只考虑了三者全在一行、时间一行剩下的两个一行两种情况
    for exp in exp_list:
        # print(exp)
        first = exp[0]
        first_list = preprocess(first)
        # print(first_list)
        time = None
        org = None
        pos = None
        desp = None
        head = ['time', 'com', 'pos', 'desp']
        # 一行包括多个信息的情况
        if len(first_list) >= 2:
            for idx, item in enumerate(first_list):
                # print(item)
                if has_time(item, itn_pattern_time) and time is None:
                    time = item
                elif is_company(item, itn_pattern_org) and org is None:
                    org = item
                elif is_position(item, itn_pattern_pos) and pos is None:
                    pos = item
                #  这里进行了一个猜测 若前几个都不是，猜测为pos
                elif pos is None:
                    pos = item
            desp = '\n'.join(exp[1:])
            # print([time, org, pos], '\n', desp)
        # 一行不到三者的情况
        elif len(first_list) == 1:
            # 每段基本上开头都是时间，判断可不加
            if has_time(first_list[0], itn_pattern_time):
                time = first_list[0]
            # 继续提取org、pos
            if len(exp) > 1:
                second = exp[1]
                second_list = preprocess(second)
                # print(second_list)
                for idx, item in enumerate(second_list):
                    if is_company(item, itn_pattern_org) and org is None:
                        org = item
                    elif is_position(item, itn_pattern_pos) and pos is None:
                        pos = item
                    #  这里进行了一个猜测 若前几个都不是，猜测为pos
                    elif pos is None:
                        pos = item
            if len(exp) > 2:
                desp = '\n'.join(exp[2:])
            # print([time, org, pos], '\n', desp)
        if sum([x is not None for x in [time, org, pos, desp]]) >= 2:
            # extract_list.append((time, org, pos, desp))
            extract_list.append(dict(zip(head, [time, org, pos, desp])))
    for item in extract_list:
        print(item)
    print(len(extract_list))
    return extract_list


def debug():
    # print(is_position("法律助理"))
    # print(is_company("富士康科技园"))
    for exp_string in exp_string_list:
        itn_time_com_pos_desp(exp_string)


if __name__ == '__main__':
    debug()





