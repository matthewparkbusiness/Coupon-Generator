from balance import Balance, Category 
from coupon import Coupon
from coupon_rule import COUPON_PRIORITY
from customer import Customer
from item import Item
from helpers import DISPLAY_WIDTH, format_money
from store import Store
from stores_manager import StoresManager
from typing import List

class Sale:
  """
  A single sale to a customer. The steps for a sale are as follows:

  1. Scanning individual items
  2. (Optional) using coupons to reduce the price
  3. Calculating and charging the amount
  4. Rewarding coupons based on items purchased
  """
  def __init__(self, customer: Customer, store: Store, store_manager: StoresManager = StoresManager()) -> None:
    self.customer = customer
    self.store = store
    self.balance = Balance()
    self.store_manager = store_manager

  def start_sale(self) -> None:
    print("=" * DISPLAY_WIDTH + f"\n{f'{self.store.name} digital checkout'.center(DISPLAY_WIDTH)}\n" + "=" * DISPLAY_WIDTH + "\n")
    print("LOGS")
    print("~" * DISPLAY_WIDTH)
    print(f"[Sale] Customer {self.customer.name} started checkout with {format_money(self.customer.balance.amount())}" \
       + f" and {len(self.customer.coupons)} coupons")

  def scan_item(self, barcode: int) -> bool:
    # Problem 1.2: YOUR CODE HERE
    if barcode in self.store.database.items.keys():
      new_item = self.store.database.items[barcode]
      self.balance.add_balance(new_item.price, new_item.category, new_item.name)
      return True
    return False

  def use_coupons(self, coupons: List[Coupon]) -> None:
    for coupon in self.sorted_coupons(coupons):
      if not coupon.rule.can_use(self.balance):
        print(f"[Coupon] Invalid - coupon {coupon.code} does not apply to this purchase")
      elif not self.customer.use_coupon(coupon):
        print(f"[Coupon] Invalid - coupon {coupon.code} was already used")
      else:
        self.balance.subtract_balance(coupon.rule.apply_discount(self.balance), category=Category.COUPON, description=f"Coupon {coupon.code} - {coupon.rule.description()}")

  def sorted_coupons(self, coupons: List[Coupon]) -> List[Coupon]:
    priority_dict = {coupon_rule : index for index, coupon_rule in enumerate(COUPON_PRIORITY)}
    return sorted(coupons, key=lambda coupon: priority_dict.get(coupon.rule, 0))

  def reward_coupons(self) -> List[Coupon]:
    # Problem 1.3: YOUR CODE HERE
    available_coupons = self.store.available_coupon_types()
    coupons_rewarded = []
    for coupon_type in available_coupons:
      num_coupons = coupon_type.number_to_reward(self.balance)
      coupons_rewarded += self.store.reward_coupons(self.customer, coupon_type, num_coupons)
    return coupons_rewarded

  def finish_sale(self) -> None:
    sale_price = self.balance.amount()
    if self.customer.balance.amount() < sale_price:
      raise Exception(f"Not enough money to complete purchase")

    self.customer.balance.subtract_balance(sale_price, description="Purchase at ____ store")
    self.balance.group_balance_items()
    print(f"\n\nSALE RESULT\n" + "~" * DISPLAY_WIDTH + "\n" + str(self.balance) + "\n")

    coupons = self.reward_coupons()
    print(f"Rewarding {len(coupons)} coupons:")
    for c in coupons:
      print(f"-> {c.rule.description()}")
    
    print(f"\nCustomer now has {format_money(self.customer.balance.amount())}" \
      + f" and {len(self.customer.coupons)} coupon(s) remaining")

    print(f"\nThanks for shopping at {self.store.name}. Please come again!\n")

