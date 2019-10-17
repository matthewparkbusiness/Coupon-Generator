from coupon_rule import FiveForFive, HalfOffHealthyPurchases, TenOffPromo
from customer import Customer
from sale import Sale
from store import Store
from store_database import StoreDatabase
from stores_manager import StoresManager
import sys

def test_full_sale():
  customer = Customer("Annie Ro")
  customer.balance.add_balance(1_012_00, description="Monthly earnings")

  store = Store("Berkeley Bowl", StoreDatabase())
  StoresManager().register_store(store)
  store.reward_coupons(customer, FiveForFive, 5)
  store.reward_coupons(customer, HalfOffHealthyPurchases, 1)

  sale = Sale(customer, store)
  sale.start_sale()
  BARCODES = ['7810', '9694', '7810', '7126', '9478', '7126', '8840', '8840', '7126', '7111']
  for code in BARCODES:
    sale.scan_item(code)
  
  sale.use_coupons(customer.coupons)

  sale.finish_sale()

def test_basic_sale():
  customer = Customer("Aivant Goyal")
  customer.balance.add_balance(10_00, description="This week's paycheck")

  store = Store("Corner Store #1", StoreDatabase())
  StoresManager().register_store(store)
  store.reward_coupons(customer, HalfOffHealthyPurchases, 1)
  store.reward_coupons(customer, TenOffPromo, 1)


  sale = Sale(customer, store)
  sale.start_sale()
  BARCODES = ['4872', '2911', '2911', '1726', '2855', '5817']
  for code in BARCODES:
    sale.scan_item(code)

  sale.use_coupons(customer.coupons)

  sale.finish_sale()


def process_args(args):
  if len(args) == 0:
    test_full_sale()
  elif args[0] == "--basic":
    test_basic_sale()
  elif args[0] == "--full":
    test_full_sale()
  else:
    print("Invalid argument. Use --basic or --full to choose test case")

