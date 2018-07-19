import json
import re

from django.core.management.base import BaseCommand


from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器


class Command(BaseCommand):

    公家內容 = {
        '來源': 'twisas-語料庫系統',
        '種類': '語句',
        '年代': '2018',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '聽拍json',  type=str
        )

    def handle(self, *args, **參數):
        self.stdout.write('資料數量：{}'.format(訓練過渡格式.資料數量()))

        全部資料 = []
        匯入數量 = 0
        漢字合音 = re.compile('（.*?）')
        with open(參數['聽拍json']) as 檔案:
            for 資料 in json.load(檔案):
                for thiann in 資料['聽拍資料']:
                    漢字 = 漢字合音.sub(
                        ' XXX ',
                        thiann['漢字'].replace('卡拉OK', '卡拉O-K')
                    )
                    句物件 = 拆文分析器.建立句物件(漢字, thiann['本調臺羅'])
                    for ji in 句物件.篩出字物件():
                        if ji.型 == 'XXX':
                            ji.型 = ji.音
                    全部資料.append(
                        訓練過渡格式(
                            文本=句物件.看分詞(),
                            **self.公家內容
                        )
                    )

                匯入數量 += 1
                if 匯入數量 % 100 == 0:
                    self.stdout.write('匯入 {} 筆'.format(匯入數量))

        self.stdout.write('檢查格式了匯入')
        訓練過渡格式.加一堆資料(全部資料)

        self.stdout.write('資料數量：{}'.format(訓練過渡格式.資料數量()))
