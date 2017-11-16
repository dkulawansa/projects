import unittest
from debit_card import (
	DebitCard, 
	DebitCardErrors,
	InsufficentFundError,
	VendorError,
	InvalidId
)

class DebitCardTests(unittest.TestCase):
	"""Test class to test DebitClass functionality"""
	def setUp(self):
		self.balance = 200
		self.acnt = DebitCard()
		self.id = '42eb703e-4231-4d6d-be90-e87f167293c2'
		self.acnt.accounts[self.id] = {'balance': float(self.balance)}
		self.vendor_id = '123'
		self.vendor_id2 = '234'
		self.vendor_id3 = '345'
		self.charge = 75
		self.hold = 25
		self.accual_amount = 125
	
	def tearDown(self):
		pass
		
	def test_create_count(self):
		id = self.acnt.create_account(1000)
		self.assertEqual(len(id), 36)
	
	def test_charge(self):
		res = self.acnt.charge(self.id, self.charge)
		self.assertEqual(res, self.balance - self.charge)
	
	def test_charge_more_than_once(self):
		res1 = self.acnt.charge(self.id, self.charge)
		self.assertEqual(res1, self.balance - self.charge)
		res2 = self.acnt.charge(self.id, 50.0)
		self.assertEqual(res2, self.balance - self.charge - 50.0)
		
	def test_charge_more_than_funds_available(self):
		charge = self.balance + 10
		with self.assertRaises(InsufficentFundError):
			self.acnt.charge(self.id, charge)
	
	def test_hold(self):
		res = self.acnt.hold(self.id, self.vendor_id, self.hold)
		self.assertEqual(res, self.balance - self.hold)
		
	def test_hold_with_charge(self):
		self.acnt.charge(self.id, self.charge)
		res = self.acnt.hold(self.id, self.vendor_id, self.hold)
		self.assertEqual(res, self.balance - self.charge - self.hold)
	
	def test_hold_more_than_funds_available(self):
		hold = self.balance + 10
		with self.assertRaises(InsufficentFundError):
			self.acnt.hold(self.id, self.vendor_id, hold)
	
	def test_one_hold_per_vender(self):
		res1 = self.acnt.hold(self.id, self.vendor_id, self.hold)
		self.assertEqual(res1, self.balance - self.hold)
		with self.assertRaises(VendorError):
			self.acnt.hold(self.id, self.vendor_id, 30.0)

	def test_hold_for_multiple_venders(self):
		res1 = self.acnt.hold(self.id, self.vendor_id, self.hold)
		self.assertEqual(res1, self.balance - self.hold)
		res2 = self.acnt.hold(self.id, self.vendor_id2, 30.0)
		self.assertEqual(res2, self.balance - self.hold - 30.0)
		res3 = self.acnt.hold(self.id, self.vendor_id3, 50.0)
		self.assertEqual(res3, self.balance - self.hold - 50.0 - 30.0)
	
	def test_settle_hold_when_actual_amount_less_than_balance(self):
		self.acnt.hold(self.id, self.vendor_id, self.hold)
		res = self.acnt.settle_hold(self.id, self.vendor_id, self.accual_amount)
		self.assertEqual(res, self.balance - self.accual_amount)
	
	def test_settle_hold_when_actual_amount_more_than_balance(self):
		self.acnt.hold(self.id, self.vendor_id, self.hold)
		with self.assertRaises(InsufficentFundError):
			self.acnt.settle_hold(self.id, self.vendor_id, 210.0)
			
if __name__ == '__main__':
	unittest.main()
