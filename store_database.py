from item import Item
from balance import Category
import csv

ITEMS_FILE = './store_items.csv'

class StoreDatabase:
  def __init__(self, filename: str = ITEMS_FILE) -> None:
    self.items = self.read_items_from_file(filename)

  def read_items_from_file(self, filename: str) -> dict:
    barcodes_to_items = {}

    with open(filename) as csvfile:
      reader = csv.reader(csvfile)
      next(reader)
      for row in reader:
        barcode, name, price, category = row
        barcodes_to_items[barcode] = Item(name, Category(category), int(price))
    
    return barcodes_to_items
