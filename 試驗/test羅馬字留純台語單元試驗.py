from unittest.case import TestCase
from 轉本調 import 比對揣出本調


class 單元試驗(TestCase):
    def tearDown(self):
        self.assertEqual(
            比對揣出本調(self.口, self.辭典),
            self.本
        )

    def test_外語(self):
        self.ku = "lan2-hong2-mng7-e5-si7-hiang1-tionn2-oh4-{-黃-玲-蘭-}"
        self.sin = "lan2-hong2-mng7-e5-si7-hiang1-tionn2-oh4 UNK"

    def test_標點符號(self):
        self.ku = "lai5-tsia1-neh5-ooh4 , tsit4-le5-sann1-ko3-gua7-gueh8-e5-si5-kan1"
        self.sin = "lai5-tsia1-neh5-ooh4 tsit4-le5-sann1-ko3-gua7-gueh8-e5-si5-kan1"
