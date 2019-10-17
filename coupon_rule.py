from abc import ABC, abstractmethod
from balance import Balance, Category

class CouponRule(ABC):
  """
  A CouponRule specifies how a particular type of coupon works. It covers:
  - When the coupon is rewarded
  - When the coupon can be applied
  - How much the coupon is worth

  Each coupon has a CouponRule associated with it. The coupon stores the rule class itself, 
  not an instance of it, since a rule is fixed and it wouldn't make sense to have many different instances.

  The Sale object uses CouponRules to decide when it should reward/accept each type of coupon.

  To create a new coupon type: 
  1. Make a subclass of the abstract CouponRule and implement the required methods.
  2. Add the new rule to COUPON_PRIORITY at the bottom of this file
  """
  @staticmethod
  @abstractmethod
  def description() -> str:
    """
    Returns a string description of the coupon (e.g. '10% off fruits').
    Can be useful for debugging or when displaying a list of the customer's coupons.
    """
    pass

  @staticmethod
  @abstractmethod
  def number_to_reward(balance: Balance) -> int:
    """
    * When rewarding coupons to customer after a sale *

    Given a Balance for the current sale, returns an integer number of coupons
    of this type that should be rewarded.
    """
    pass

  @staticmethod
  @abstractmethod
  def can_use(balance: Balance) -> bool:
    """
    * When customer wants to use coupons towards a sale *

    Given a Balance for the current sale, returns whether this coupon can apply.
    """
    pass

  @staticmethod
  @abstractmethod
  def apply_discount(balance: Balance) -> int:
    """
    Returns the amount (in cents) that the sale price should be discounted by.

    The Balance is provided in case the coupon applies a discount only for specific items (e.g. fruits)
      and/or individual BalanceItems need to be modified as a result of the coupon being applied.
      This means this function (unlike the others) does not necessarily need to be pure!

    NOTE: This method does NOT validate whether the coupon can actually be applied. It is assumed
      that `can_use(balance)` was already checked beforehand.
    """
    pass


##############################################
##              COUPON RULES                ##
##############################################

class HalfOffHealthyPurchases(CouponRule):
  """
  50% off entire purchase if spending $20 or more on fruits. Cannot be used with any other coupon.
  This coupon is rewarded when the customer buys one or more fruit items.
  """
  @staticmethod
  def description():
    return "50% off when you spend $20 or more on fruits"

  @staticmethod
  def number_to_reward(balance):
    valid_items = balance.balance_items_with_category(Category.FRUITS)
    return len(valid_items) > 0

  @staticmethod
  def can_use(balance):
    return len(balance.balance_items_with_category(Category.COUPON)) == 0 and \
      HalfOffHealthyPurchases.__fruit_value(balance) >= 20_00

  @staticmethod
  def apply_discount(balance):
    return balance.amount() // 2

  # Helper methods
  # ---------------
  
  @staticmethod
  def __fruit_value(balance):
    valid_items = balance.balance_items_with_category(Category.FRUITS)
    return sum([item.amount for item in valid_items])

class TenOffPromo(CouponRule):
  """
  A one-time $10 off coupon given to new customers in order to encourage them to use DC Central Kitchen
  partner stores.
  This coupon is NOT ever rewarded during a purchase.
  """
  @staticmethod
  def description():
    return "$10 off your first purchase!"

  @staticmethod
  def number_to_reward(balance):
    return 0

  @staticmethod
  def can_use(balance):
    return True

  @staticmethod
  def apply_discount(balance):
    return min(10_00, balance.amount())

class FiveForFive(CouponRule):
  """
  5 for 5 program: $5 off fruits and veggies.
  This coupon is rewarded when the customer spends $5 or more on a purchase (max 1 coupon rewarded per purchase)
  """
  # Problem 2.1: YOUR CODE HERE
  @staticmethod
  def description():
    return "$5 off fruits and veggies"

  @staticmethod
  def number_to_reward(balance):
    if sum([item.amount for item in balance.balance_items]) >= 5_00:
      return 1
    return 0

  @staticmethod
  def can_use(balance):
    discounted_items = balance.balance_items_with_category(Category.FRUITS) + balance.balance_items_with_category(Category.VEGGIES)
    total_discount = 0
    for item in discounted_items:
      total_discount += item.amount - item.discounted
    return total_discount != 0

  @staticmethod
  def apply_discount(balance):
    discounted_items = balance.balance_items_with_category(Category.FRUITS) + balance.balance_items_with_category(Category.VEGGIES)
    total_discount = 0
    for item in discounted_items:
      total_discount += item.amount - item.discounted
      if total_discount > 5_00:
        item.discounted = item.amount - (total_discount - 5_00)
        total_discount = 5_00
        break
      else:
        item.discounted = item.amount
    return min(total_discount, balance.amount())


# Lists the "priority" of all coupon types from highest to lowest.
# If the customer uses more than one coupon in a Sale, higher priority coupons get applied first.
COUPON_PRIORITY = [
  TenOffPromo,
  HalfOffHealthyPurchases
]