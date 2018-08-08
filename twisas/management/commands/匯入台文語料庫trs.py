import json
from urllib.request import urlopen

from django.core.management.base import BaseCommand


from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from os import walk
from os.path import dirname


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
        檔案所在 = {}
        for 這馬所在, _, 檔名陣列 in walk(dirname(參數['trs聽拍json'])):
            for 檔名 in 檔名陣列:
                檔案所在[檔名] = join(這馬所在, 檔名)

        for tsua in self._tongan資料(參數['trs聽拍json']):
            tsua['內容'] = tsua['口語臺羅']
            全部資料.append(
                訓練過渡格式(
                    影音=檔案所在[tsua["檔名"].replace('trs', 'wav')],
                    聽拍=[tsua],
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
            return json.load(檔)
