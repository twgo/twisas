import json
from os import walk
from os.path import dirname, join

from django.core.management.base import BaseCommand
from twisas import 留台語


from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器


class Command(BaseCommand):
    valid_dataset = []
    test_dataset = ['NB-15.trs','PN-18.trs']

    公家內容 = {
        '來源': 'twisas-trs',
        '種類': '語句',
        '年代': '2018',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '羅馬字', choices=['口語', '本調'],
        )
        parser.add_argument(
            'dataset', choices=['train', 'valid', 'test']
        )
        parser.add_argument(
            '--提掉外來詞', action='store_true'
        )
        parser.add_argument(
            'trs聽拍json',  type=str
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
            if self.有欲匯無(參數['dataset'], tsua["檔名"]):
                if 參數['羅馬字'] == '口語':
                    羅馬字 = (
                        tsua['口語臺羅']
                        .replace(' -', ' ').replace('- ', ' ').strip('-')
                    )
                else:
                    羅馬字 = tsua['本調臺羅']
                分詞 = 拆文分析器.建立句物件(羅馬字).看分詞()
                if 參數['提掉外來詞']:
                    tsua['內容'] = 留台語(分詞)
                else:
                    tsua['內容'] = 分詞
                tsua['開始時間'] = float(tsua['開始時間'])
                tsua['結束時間'] = float(tsua['結束時間'])
                全部資料.append(
                    訓練過渡格式(
                        影音所在=檔案所在[tsua["檔名"].replace('trs', 'wav')],
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

    def 有欲匯無(self, dataset, 檔名):
        if dataset == 'valid':
            return 檔名 in self.valid_dataset
        if dataset == 'test':
            return 檔名 in self.test_dataset
        return 檔名 not in self.valid_dataset and 檔名 not in self.test_dataset
