from coupon import Coupon
from coupon_rule import CouponRule
from typing import Type
import string, random

class CouponGenerator:
  MIN_CODE_LENGTH = 5

  def __init__(self, code_length: int) -> None:
    random.seed("BLUEPRINT")
    
    self.coupon_codes = set()
    assert code_length >= CouponGenerator.MIN_CODE_LENGTH, f"Coupon code length must be at least {CouponGenerator.MIN_CODE_LENGTH}!"
    self.code_length = code_length
    self.__max_coupons = 26 ** self.code_length

  def generate_coupon(self, rule: Type[CouponRule]) -> Coupon:
    if len(self.coupon_codes) >= self.__max_coupons:
      raise Exception(f"[CouponGenerator] Generated the max possible # of coupons for length {self.code_length} codes")

    while True:
      new_code = self.__get_code()
      if not new_code in self.coupon_codes:
        self.coupon_codes.add(new_code)
        break

    coupon = Coupon(rule, new_code)
    return coupon

  def __get_code(self) -> str:
    alphabet = string.ascii_uppercase
    return ''.join(random.choice(alphabet) for i in range(CouponGenerator.MIN_CODE_LENGTH))
