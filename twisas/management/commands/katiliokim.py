import os
from os.path import join


from 臺灣言語服務.models import 訓練過渡格式
from 匯入.指令 import 匯入枋模
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器


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
        匯入數量 = 0
        for 所在, _資料夾陣列, 檔案陣列 in sorted(os.walk(參數['所在'])):
            for tong in 檔案陣列:
                if tong.endswith('_trans_utf8.txt'):
                    with open(join(所在, tong)) as thak:
                        for tsua in thak.readlines():
                            if tsua.rstrip() != '':
                                mia, tl = tsua.rstrip().split(' ', 1)
                                yield 訓練過渡格式(
                                    影音所在=join(所在, mia),
                                    文本=拆文分析器.建立句物件(tl.split('//', 1)[1]).看型('-',' '),
                                    **self.公家內容
                                )

                    匯入數量 += 1
                    if 匯入數量 % 100 == 0:
                        self.stdout.write('匯入 {} 筆'.format(匯入數量))
