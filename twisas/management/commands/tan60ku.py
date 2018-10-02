from os.path import join


from 臺灣言語服務.models import 訓練過渡格式
from 匯入.指令 import 匯入枋模
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from csv import DictReader
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


class Command(匯入枋模):

    公家內容 = {
        '來源': 'Kati',
        '種類': '語句',
        '年代': '2018',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '所在',  type=str
        )

    def 全部資料(self, *args, **參數):
        with open(join(參數['所在'], '聽拍.csv')) as csvtong:
            for tsua in DictReader(csvtong):
                句物件 = 拆文分析器.建立句物件(tsua['本調臺羅'].strip()).轉音(臺灣閩南語羅馬字拼音,'轉通用拼音')
                su=[]
                for 詞物件 in 句物件.網出詞物件():
                    if not 詞物件.敢是標點符號():
                        su.append(詞物件.看型('-', ' '))

                yield 訓練過渡格式(
                    影音所在=join(參數['所在'], tsua['檔名']),
                    文本=' '.join(su),
                    **self.公家內容
                )

                # tsua['口語調臺羅']
