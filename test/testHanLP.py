import re
import hanlp
# 分句
# string="2017.06 中国工商银行校园商战大赛 优胜奖（全国前 30%）"
# dengstr=re.sub(r' *\n','##',string)
# dengstr=re.sub(r'#{2,}','',dengstr)
# dengstr=re.findall(r'.{100}',dengstr)
# print(dengstr)

string = """2013.10-至今       广州银行                 营业部柜员"""
string1 = "2011.7-2013.9      广发银行                 营业部开户业务 "
string2 = "2010.10-2011.6     东亚银行（中国）有限公    营业部柜员 "
string3 = "2015.06  为南阳市桐柏县阳光半岛房地产项目制作“桐柏醉美啤酒节”主题微信宣传页面和抽奖活动程序；"
string4 = "2014.6-2015.5         中南财经政法大学财政税务学院学生会             学术部副部长"
string5 = "2014.9-2016.1         中南财经政法大学财政税务学院学生助教中心       助教兼负责人 "
string6 = "2016.12-2017.3        瑞华会计师事务所（特殊普通合伙）深圳分所       审计助理 "

recognizer = hanlp.load(hanlp.pretrained.ner.MSRA_NER_BERT_BASE_ZH)
res = recognizer(list(string5))
print(res)
