from coupon import Coupon
from coupon_rule import CouponRule
from customer import Customer
from helpers import NAMESPACE_ID
from store_database import StoreDatabase
from typing import List, Type
import uuid

class Store:
  def __init__(self, name: str, database: StoreDatabase) -> None:
    self.uuid = uuid.uuid5(NAMESPACE_ID, name)
    self.name = name
    self.database = database
    self.coupon_inventory = {}

  def add_coupons_to_inventory(self, coupons: List[Coupon], rule: Type[CouponRule]) -> None:
    self.coupon_inventory[rule] = self.coupon_inventory.get(rule, []) + coupons

  def available_coupon_types(self) -> List[Type[CouponRule]]:
    return list(filter(lambda rule: len(self.coupon_inventory[rule]) > 0, self.coupon_inventory.keys()))

  def reward_coupons(self, customer: Customer, rule: Type[CouponRule], num: int) -> List[Coupon]:
    # Problem 1.3: YOUR CODE HERE
    if rule in self.available_coupon_types():
      if len(self.coupon_inventory[rule]) <= num:
        coupons_rewarded = self.coupon_inventory[rule]
        self.coupon_inventory[rule] = []
      else:
        coupons_rewarded = self.coupon_inventory[rule][0:num]
        self.coupon_inventory[rule] = self.coupon_inventory[rule][num: len(self.coupon_inventory[rule])]
      customer.add_coupons(coupons_rewarded)
      return coupons_rewarded

    return []

  def __hash__(self) -> int:
    return hash(self.uuid)

  def __eq__(self, other: 'Store') -> bool:
    return self.uuid == other.uuid
