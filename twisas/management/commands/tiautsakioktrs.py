import json
from os import walk
from os.path import join

from trs import 讀trs


from 匯入.指令 import 匯入枋模


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
                    with open(join(sootsai, '{}.json'.format(tongan)), 'w') as jtong:
                        json.dump(
                            讀trs(join(sootsai, tongan)),
                            jtong,
                            ensure_ascii=False, indent=2, sort_keys=True
                        )
        return []
