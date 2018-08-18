from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


def 留台語(trs_ku):
    句物件 = 拆文分析器.分詞句物件(trs_ku)
    詞陣列 = []
    毋知 = False
    for 詞物件 in 句物件.網出詞物件():
        字陣列 = []
        for 字物件 in 詞物件.篩出字物件():
            if 字物件.敢是標點符號():
                毋知 = False
            elif 臺灣閩南語羅馬字拼音(字物件.型).音標:
                字陣列.append(字物件.看分詞())
                毋知 = False
            elif 毋知:
                pass
            else:
                毋知 = True
                詞陣列.append('-'.join(字陣列))
                詞陣列.append("UNKS")
                字陣列 = []
        詞陣列.append('-'.join(字陣列))
    kiatko = []
    for 詞 in 詞陣列:
        if 詞 != '':
            kiatko.append(詞)
    return ' '.join(kiatko)
