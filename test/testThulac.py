from thulac import thulac
lac=thulac(filt=True)
string = """2013.10-至今       广州银行                 营业部柜员"""
res=lac.cut(string)
time=[]
org=[]
loc=[]
per=[]
for item in res:
    if item[1] == 'np':
        per.append(item[0])
    elif item[1] == 'ns':
        loc.append(item[0])
    elif item[1] == 't':
        time.append(item[0])
    elif item[1] == 'ni':
        org.append(item[0])
print(org)
print(time)
print(per)
print(loc)