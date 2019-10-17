from coupon_rule import CouponRule
from typing import Type

class Coupon:
  def __init__(self, rule: Type[CouponRule], code: str) -> None:
    self.rule = rule
    self.code = code
    self.used = False

  def use(self) -> bool:
    result = not self.used
    self.used = True
    return result

  def __repr__(self) -> str:
    return f"Coupon {self.code}{' [USED]' if self.used else ''}: {self.rule.description()}"

  def __hash__(self) -> int:
    return hash(self.code)
