from extracter import Extracter
from provider import Provider
from constant import *
from icecream import ic
import unittest

class TestProvider(unittest.TestCase):
  def setUp(self):
    ic.disable()
    self.ranges = [
      (1714126400, 1714780799),
      (1714780800, 1714880799),
      (1714880800, 1714953600)
    ]
    Provider.init()
    Extracter.addresses(SMART)
    Extracter.addresses(FRENS)

  def test_1_set_range(self):
    (
      Provider
        .set_range(*self.ranges[0])
        .check(Provider.start_block == '62998044')
        .check(Provider.end_block == '63325243')
        .set_range(*self.ranges[1])
        .check(Provider.start_block == '63325244')
        .check(Provider.end_block == '63375243')
        .set_range(*self.ranges[2])
        .check(Provider.start_block == '63375244')
        .check(Provider.end_block == '63411644')
    )

  def test_2_get_txn_in_range(self):
    (
      Provider
        .set_range(*self.ranges[1])
        .get_txn_in_range(Extracter.addresses())
        .check(len(Extracter.addresses()) == 6)
    )

  def test_3_txn_exist_in_range(self):
    (
      Provider
        .set_range(*self.ranges[2])
        .txn_exist_in_range(Extracter.addresses())
        .check(len([value for value in Extracter.addresses().values() if value == True]) == 6)
    )