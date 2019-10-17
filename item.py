from balance import Category

class Item:
  def __init__(self, name: str, category: Category, price: int) -> None:
    self.name = name
    self.category = category
    self.price = price

  def __repr__(self) -> str:
    return f"{self.name} ({self.category}) - {self.price}"
