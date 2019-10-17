from helpers import format_money, DISPLAY_WIDTH
import balance

class BalanceItem:
  """
  Represents a single change (positive or negative) to a balance
  """
  def __init__(self, amount: int, category: 'Category', description: str) -> None:
    self.amount = amount
    self.category = category
    self.description = description
    self.discounted = 0

  def __str__(self) -> str:
    return f"{(self.description + ' ').ljust(DISPLAY_WIDTH - 10, '.')} {format_money(self.amount, sign=True)}"

  """
  EXPLANATION FOR PART 3
  In group_balance_items() from Balance, Counter is used to group equal BalanceItems. However, with
  the bug, two BalanceItems that are the same (for instance two Potatoes) are not grouped, since they
  are not equal to Counter. Therefore, we must override the __eq__ and __hash__ functions to tell Counter
  that two BalanceItems with the same descriptions are equal. I chose to do it this way, since two BalanceItems
  are in reality equal if they have the same description, so it makes perfect sense for __eq__ and __hash__
  to compare the descriptions. This allows comparing two BalanceItems to be done correctly in Counter.
  """
  def __eq__(self, other):
    return self.description == other.description

  def __hash__(self):
    return hash(self.description)
