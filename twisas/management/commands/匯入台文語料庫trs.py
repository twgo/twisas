import json
from urllib.request import urlopen

from django.core.management.base import BaseCommand


from 臺灣言語服務.models import 訓練過渡格式


class Command(BaseCommand):
    help = '匯入高明達聽拍的twisas資料庫'

    公家內容 = {
        '來源': '台文資料庫trs',
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
            全部資料 = self._tongan資料(參數['trs聽拍json'])
        else:
            全部資料 = self._github資料()
        for 資料 in 全部資料:
            全部資料.append(
                訓練過渡格式(
                    文本=資料,
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
