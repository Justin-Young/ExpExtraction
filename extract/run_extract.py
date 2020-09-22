from extract.internship import *
from extract.campus import *


def extract_from_file(file_path, itn_label='InternExp', cps_label='CampusExp'):
    """
    对分完类的文件进行校外校内经历的抽取，对时间、[公司]、岗位、描述等信息的提取

    :param file_path: 分完类的文件
    :param itn_label: 校外经历的label
    :param cps_label: 校内经历的label
    :return: 返回一个元组，校外经历和校内经历，每个经历是一个列表，其元素是一个字典，
             校外经历为四项 time、com、pos、desp,校内为三项 time、pos、desp
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
        sentns = txt.split('\n')
        itn_exp = []
        cps_exp = []
        itn = None
        cps = None
        for item in sentns:
            temp = re.split(r'(?:(?: {4,})|(?:\t+))', item, maxsplit=1)
            # print("item:", item)
            # print("temp:", temp)
            if len(temp) >= 2:
                lbl = temp[0]
                sentn = temp[1]
                # print("lbl:", lbl)
                # print("sentn", sentn)
                if sentn is not None:
                    if lbl.find(itn_label) != -1 :
                        itn_exp.append(sentn)
                    elif lbl.find(cps_label) != -1 :
                        cps_exp.append(sentn)
    if len(itn_exp):
        # print("itn_exp", itn_exp)
        itn = itn_time_com_pos_desp('\n'.join(itn_exp))
    if len(cps_exp):
        # print("cps_exp", cps_exp)
        cps = cps_time_pos_desp('\n'.join(cps_exp))
    return itn, cps


if __name__ == '__main__':
    extract_from_file('../other/1.txt')
    extract_from_file('../other/0.txt')
