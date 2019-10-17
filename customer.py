from balance import Balance
from coupon import Coupon
from helpers import NAMESPACE_ID
from typing import List
import uuid

class Customer:
  def __init__(self, name: str) -> None:
    self.uuid = uuid.uuid5(NAMESPACE_ID, name)
    self.name = name
    self.coupons = set()
    self.balance = Balance()

  def add_coupons(self, coupons: list) -> None:
    self.coupons.update(coupons)

  def use_coupon(self, coupon: Coupon) -> bool:
    if not coupon in self.coupons:
      raise Exception(f"Customer tried to use coupon {coupon.code} but does not own it")
    did_use = coupon.use()
    self.coupons.remove(coupon)
    return did_use

  def get_all_coupons(self) -> List[Coupon]:
    return sorted(list(self.coupons), key=lambda c: c.rule.description())

  def __hash__(self):
    return hash(self.uuid)