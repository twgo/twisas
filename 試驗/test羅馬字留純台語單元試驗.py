from unittest.case import TestCase

from twisas import 留台語


class 單元試驗(TestCase):
    def tearDown(self):
        self.assertEqual(
            留台語(self.ku),
            self.sin
        )

    def test_外語(self):
        self.ku = "lan2-hong2-mng7-e5-si7-hiang1-tionn2-oh4-{-黃-玲-蘭-}-lah"
        self.sin = "lan2-hong2-mng7-e5-si7-hiang1-tionn2-oh4 UNKS lah"

    def test_外語分開(self):
        self.ku = "lan2-hong2-mng7-e5-si7-hiang1-tionn2-oh4 { 黃玲蘭 } lah"
        self.sin = "lan2-hong2-mng7-e5-si7-hiang1-tionn2-oh4 UNKS lah"
    def test_標點符號(self):
        self.ku = "lai5-tsia1-neh5-ooh4 , tsit4-le5-sann1-ko3-gua7-gueh8-e5-si5-kan1"
        self.sin = "lai5-tsia1-neh5-ooh4 tsit4-le5-sann1-ko3-gua7-gueh8-e5-si5-kan1"
