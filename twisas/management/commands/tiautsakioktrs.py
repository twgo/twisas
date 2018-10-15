from os import walk
from os.path import join

from trs import 讀trs


from 臺灣言語服務.models import 訓練過渡格式
from 匯入.指令 import 匯入枋模
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


class Command(匯入枋模):

    公家內容 = {
        '來源': 'tiautsakioktrs',
        '種類': '語句',
        '年代': '2018',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '所在',  type=str
        )

    def 全部資料(self, *args, **參數):
        for sootsai, _giap, tongantui in sorted(walk(參數['所在'])):
            for tongan in tongantui:
                if tongan.endswith('.trs'):
                    aie = []
                    for ku in 讀trs(join(sootsai, tongan)):
                        try:
                            tl = ku['trs聽拍'].split('//')[1].strip()
                        except IndexError:
                            pass
                        else:
                            句物件 = 拆文分析器.建立句物件(tl).轉音(臺灣閩南語羅馬字拼音)
                            sin = {
                                '開始時間': float(ku['開始時間']),
                                '結束時間': float(ku['結束時間']),
                                '內容': 句物件.看型('-', ' '),
                                '語者': '無註明',
                            }
                            aie.append(sin)
                    mia = tongan.split('-')[0]
                    yield 訓練過渡格式(
                        影音所在=join(sootsai, '{}.wav.pcm.wav'.format(mia)),
                        聽拍=aie,
                        **self.公家內容
                    )
