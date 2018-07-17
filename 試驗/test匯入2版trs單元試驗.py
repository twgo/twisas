
from django.core.management import call_command
from django.test.testcases import TestCase


from 臺灣言語服務.models import 訓練過渡格式


class 匯入2版trs單元試驗(TestCase):
    def test_匯入數量(self):
        call_command('匯入台文語料庫trs')
        self.assertGreater(訓練過渡格式.資料數量(), 13000)
