## 提取函数
    1. extrvct.internship.itn_time_com_pos_desp(exp_string)
        输入为校外经历字符串，输出为经历列表，每个元素是字典类型time,org,pos,desp
    2. extract.campus.cps_time_pos_desp(exp_string)
        输入为校内经历字符串，输出为经历列表，每个元素是字典类型，包含三项time,pos,desp
## 依赖包
    pip install lac
## 其他
    1. 若要运行建议单独测试internship、campus，run_extract是为了修改接口，并不完善
    2. 目录test下尝试了其他包，诸如HanLP、stanza、thulac、ltp,可能会因为缺少包报错可以直接删除
    3. other里面保存了一些公司名称，文件较大，相对较全，用于使用扩展选项进行查表操作（默认关闭），可修略改代码开启选项
    4. 由于采用纯规则，结果与规则和文档排版格式关系密切，目前在少部分样本较中表现还可以（不会比一般的机器学习差，但比人工还有不小距离）
        后续可能需要升级规则，规则以全局变量形式声明与文件头，方便修改
    