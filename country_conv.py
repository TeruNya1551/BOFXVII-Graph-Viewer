
# 将主催用的ISO2国家代码转化为标准国家名称

import country_converter as coco

def convert(ISO2_):
    return coco.convert(ISO2_, to='name_short')

def list_convert(list):
    newList = []
    for ISO2 in list:
        ISO2 = convert(ISO2)
        newList.append(ISO2)
    return newList