from os.path import join
from posix import listdir

from trs import 讀trs


from 臺灣言語服務.models import 訓練過渡格式
from 匯入.指令 import 匯入枋模
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
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
        for tong in sorted(listdir(參數['所在'])):
            if tong.endswith('trs') and tong.startswith('twn'):
                aie = []
                for ku in 讀trs(join(參數['所在'], tong)):
                    try:
                        tl = ku['trs聽拍'].split('//')[1].strip()
                    except IndexError:
                        pass
                    else:
                        句物件 = 拆文分析器.建立句物件(tl).轉音(臺灣閩南語羅馬字拼音)
                        su = []
                        for 詞物件 in 句物件.網出詞物件():
                            if not 詞物件.敢是標點符號():
                                su.append(詞物件.看型('-', ' '))
                        sin = {
                            '開始時間': float(ku['開始時間']),
                            '結束時間': float(ku['結束時間']),
                            '內容': ' '.join(su),
                            '語者': '無註明',
                        }
                        aie.append(sin)
                yield 訓練過渡格式(
                    影音所在=join(參數['所在'], '{}.wav'.format(
                        tong.split('.')[0])),
                    聽拍=aie,
                    **self.公家內容
                )
