import json
from urllib.request import urlopen

from django.core.management.base import BaseCommand


from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器


class Command(BaseCommand):

    公家內容 = {
        '來源': 'twisas-trs',
        '種類': '語句',
        '年代': '2018',
    }
    trs網址 = 'https://twgo.github.io/Taigi_giliau_HL/twisas-HL.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '--trs聽拍json',  type=str
        )

    def handle(self, *args, **參數):
        self.stdout.write('資料數量：{}'.format(訓練過渡格式.資料數量()))

        全部資料 = []
        匯入數量 = 0
        if 參數['trs聽拍json']:
            guan資料 = self._tongan資料(參數['trs聽拍json'])
        else:
            guan資料 = self._github資料()
        for han in guan資料:
            句物件 = 拆文分析器.建立句物件(han)
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

    def _tongan資料(self, tongan):
        with open(tongan) as 檔:
            資料 = json.load(檔)
        for tsua in 資料:
            yield tsua['漢字']

    def _github資料(self):
        with urlopen(self.trs網址) as 檔:
            資料 = json.loads(檔.read().decode())
        for tsua in 資料:
            yield tsua['漢字']
