from extract.internship import *
from extract.campus import *


def main(string, is_itn):
    """
    对字符串进行信息抽取，对时间、[公司]、岗位、描述等信息的提取

    :param string: 待提取信息的字符串
    :param is_itn: 是否为校外经历
    :return: 返回经历列表，元素是一个元组，校外经历为四元组、校内为三元组
    """
    if is_itn:
        res = itn_time_org_pos_depict(string)
    else:
        res = cps_time_pos_depict(string)


if __name__ == '__main__':
    main(string1, True)
