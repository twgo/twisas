from os import walk
from os.path import join, abspath
from shutil import copyfile

from django.conf import settings


from 匯入.指令 import 匯入枋模
from 臺灣言語服務.models import 訓練過渡格式
from 臺灣言語服務.kaldi.lexicon import 辭典輸出
from 臺灣言語服務.Kaldi語料匯出 import Kaldi語料匯出
from 臺灣言語工具.系統整合.程式腳本 import 程式腳本


class Command(匯入枋模):

    公家內容 = {
        '來源': 'tiautsakioktrs',
        '種類': '語句',
        '年代': '2018',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            'kaldis5c',  type=str
        )
        parser.add_argument(
            '所在',  type=str
        )

    def 全部資料(self, *args, **參數):
        訓練過渡格式.objects.all().delete()
        服務設定 = settings.HOK8_BU7_SIAT4_TING7['台語']
        for sootsai, _giap, tongantui in sorted(walk(參數['所在'])):
            for tongan in tongantui:
                if tongan.endswith('.pcm.wav'):
                    訓練過渡格式.objects.create(影音所在=join(sootsai, tongan), 文本='文本')
                    辭典輸出物件 = 辭典輸出(服務設定['音標系統'], '拆做聲韻')
                    Kaldi語料匯出.匯出一種語言語料(
                        '台語', 辭典輸出物件,
                        'vad', 's5c',  Kaldi語料匯出.初使化辭典資料()
                    )
                    訓練過渡格式.objects.all().delete()
                    資料 = abspath('vad/s5c/train')
                    with 程式腳本._換目錄(參數['kaldis5c']):
                        程式腳本._走指令(['./vad.sh', 資料])
                    copyfile(
                        'vad/s5c/train_segmented/segments',
                        join(sootsai, '{}.seg'.format(tongan[:-8]))
                    )

        return []
