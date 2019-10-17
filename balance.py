from balance_item import BalanceItem
from collections import Counter
from helpers import DISPLAY_WIDTH, format_money
from enum import Enum
from typing import List

class Category(Enum):
  VEGGIES = "Veggies"
  DAIRY = "Dairy"
  SNACKS = "Snacks"
  FRUITS = "Fruits"
  DRINKS = "Drinks"
  KITCHEN = "Kitchen"
  HEALTH = "Health"
  COUPON = "Coupon"
  OTHER = "Other"

class Balance:
  """
  A Balance is a running total for a transaction. It tracks all the additions and deductions that were
  made (through BalanceItems) and allows for filtering based on category.
  """
  def __init__(self) -> None:
    self.cached_amount = 0
    self.balance_items = []
    self.dirty = False

  def add_balance(self, amount: int, category: Category = Category.OTHER, description: str = "Add money") -> None:
    self.balance_items += [BalanceItem(amount, category, description)]
    self.dirty = True

  def subtract_balance(self, amount: int, category: Category = Category.OTHER, description: str = "Subtract money") -> None:
    self.balance_items += [BalanceItem(-amount, category, description)]
    self.dirty = True

  def clear_balance(self) -> None:
    self.balance_items = []
    self.dirty = True

  def balance_items_with_category(self, category: Category) -> List[BalanceItem]:
    return list(filter(lambda item: item.category == category, self.balance_items))

  def amount(self) -> int:
    if self.dirty:
      total = sum([item.amount for item in self.balance_items])
      self.dirty = False
      self.cached_amount = total
    return self.cached_amount

  def group_balance_items(self) -> None:
    """
    Groups items so that they look nicer in the final purchase list.
    For example, 3 separate BalanceItems for apples will turn into a single item that says 'Apple (x3 @ 199 each)'.
    This permanently changes the items belonging to this balance!!
    """
    counts = Counter(self.balance_items)
    self.clear_balance()
    for item in counts:
      quantity_str = f" (x{counts[item]} @ {format_money(item.amount)} each)" if counts[item] > 1 else ""
      self.add_balance(item.amount * counts[item], category=item.category, description=f"{item.description}{quantity_str}")
    self.dirty = False  # No need to recalculate; total is the same

  def __str__(self) -> str:
    result = ""
    for item in self.balance_items:
      result += f"{item}\n"
    result += "=" * DISPLAY_WIDTH + "\n"
    result += f"{'TOTAL:'.ljust(DISPLAY_WIDTH - 9)} {format_money(self.amount())}\n"
    result += "=" * DISPLAY_WIDTH
    return result
  