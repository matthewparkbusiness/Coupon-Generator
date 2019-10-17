import unittest
from balance import Balance, Category
from coupon_rule import HalfOffHealthyPurchases, FiveForFive

class FiveForFiveTests(unittest.TestCase):
  # Problem 2.2: YOUR CODE HERE

  def test_five_for_five_can_use(self):
    b = Balance()
    b.add_balance(1_20, Category.DAIRY)
    b.add_balance(4_34, Category.DRINKS)
    self.assertFalse(FiveForFive.can_use(b))

    b.add_balance(0, Category.VEGGIES, "carrot")
    b.add_balance(0, Category.FRUITS, "grapes")
    self.assertFalse(FiveForFive.can_use(b))

    b.add_balance(3_50, Category.FRUITS, "apple")
    b.add_balance(3_50, Category.FRUITS, "banana")
    self.assertTrue(FiveForFive.can_use(b))

  def test_five_for_five_number_to_reward(self):
    b = Balance()
    b.add_balance(1_00, Category.DAIRY, "milk")
    self.assertEqual(FiveForFive.number_to_reward(b), 0, "If the total price is less than $5.00, we reward 0 "
                                                          "FiveForFive coupons.")
    b.add_balance(6_00, Category.DRINKS, "orange juice")
    self.assertEqual(FiveForFive.number_to_reward(b), 1, "If the total price is more than $5.00, we reward only 1 "
                                                          "FiveForFive coupon.")

  def test_five_for_five_apply_discount(self):
    b = Balance()
    b.add_balance(2_30, Category.FRUITS, "watermelon")
    b.add_balance(6_00, Category.VEGGIES, "lettuce")
    self.assertEqual(FiveForFive.apply_discount(b), 5_00, "If the total price of fruits and veggies is greater than "
                                                           "$5.00, we discount $5.00 from the price")
    self.assertEqual(FiveForFive.apply_discount(b), 3_30, "If the price so far of fruits and veggies is less than "
                                                           "$5.00 but still greater than $0.00, we discount the"
                                                           "remaining price of fruits and veggies. This is meant to "
                                                           "test whether we can track the discounted fruits and "
                                                           "veggies so far.")

class HalfOffHealthyPurchasesTests(unittest.TestCase):
  def test_basic_discount(self):
    # Adding $20 worth of fruits
    b = Balance()
    b.add_balance(10_00, Category.FRUITS, "a very expensive apple")
    b.add_balance(3_00, Category.OTHER, "a frog")
    b.add_balance(6_00, Category.FRUITS, "organic cage-free grapes")
    b.add_balance(12_00, Category.VEGGIES, "beef")
    self.assertFalse(HalfOffHealthyPurchases.can_use(b))

    b.add_balance(4_00, Category.FRUITS, "do fruit snacks count as fruit?")
    self.assertTrue(HalfOffHealthyPurchases.can_use(b))

  def test_using_other_coupons(self):
    # Already used another coupon => can't apply this coupon type
    b = Balance()
    b.add_balance(25_00, Category.FRUITS, "yum")
    self.assertTrue(HalfOffHealthyPurchases.can_use(b))

    b.subtract_balance(0, Category.COUPON, "the worst coupon ever")
    self.assertFalse(HalfOffHealthyPurchases.can_use(b))

if __name__ == '__main__':
    unittest.main()