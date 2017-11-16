"""
Challenge
Create an application that mimics a simplistic debit card system. For our purposes, account
information is stored in memory only, and will be lost when the application exits.
One feature of these accounts is special support for restaurants. After a customer provides their
credit card to pay for a meal, the server does not know how large a tip they will leave if they choose
to leave one on the card. The restaurant's credit card terminal is typically set to authorize (hold) the
cost of the meal, but the transaction will settle for the actual total including the actual tip written
on the receipt.

Supported​ ​Actions
● create_account (initial balance)
	○ creates a new account with an initial balance, and returns the new account_id
● charge(account_id, amount)
	○ A regular charge to the card, without a hold. Debits the balance on the account.
● hold(account_id, vendor_id, amount)
	○ places a hold on the amount requested
● settle_hold(account_id, vendor_id, actual_amount)
	○ releases the hold, and debits the actual amount
Details
	● If a charge or hold is requested, and there are insufficient funds, the transaction is rejected,
	and the balance is unchanged.
	● When a hold is requested, the held funds are not available. Only one hold per vendor id per
	account.
	● When settle_hold is called, the original hold is released, and the actual_amount is charged to
	the account. If the actual_amount exceeds available funds, the transaction is declined and
	the held funds are released.
	● The code should be unit tested, and kept as clean and simple as possible.
	● The format of the requests and responses is up to you.
	● If you like, you can create a command line interface, but it is fine to show that the
	application works correctly through unit tests alone.
"""


import uuid
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DebitCardErrors(Exception):
	"""Debit Card Base exceptions  """

class InsufficentFundError(DebitCardErrors):
	"""Insufficent funds Error"""

class VendorError(DebitCardErrors):
	"""One hold per vendor id per account"""
	
class InvalidId(DebitCardErrors):
	"""Invalid credicard id"""

class DebitCard:
	""" Simple debit card system """
	
	def __init__(self):
		""" store data in a dict in memory """
		self.accounts = {}

	def create_account (self, initial_balance):
		""" create an accout with initial balance """
		
		id = str(uuid.uuid4())
		self.accounts[id] = {'balance': float(initial_balance)}
		return id
	
	def charge(self, account_id, amount):
		""" charge to the account """
		
		# If a charge is requested, and there are insufficient funds, 
		# the transaction is rejected, and the balance is unchanged.
		if self.accounts.get(account_id, None):
			if amount <= self.accounts[account_id].get('balance', 0):
				self.accounts[account_id]['balance'] -= float(amount)
			else:
				logger.info("Insufficent funds to charge, tranaction rejected")
				raise InsufficentFundError("Insufficent funds to charge, tranaction rejected")
			return self.accounts[account_id]['balance']

	def hold(self, account_id, vendor_id, amount):
		""" hold funds until relase """
		# If hold is requested, and there are insufficient funds, 
		# the transaction is rejected, and the balance is unchanged.
		# When a hold is requested, the held funds are not available. 
		# Only one hold per vendor id per account
		
		if self.accounts.get(account_id, None):

			if all([amount <= self.accounts[account_id].get('balance', 0), vendor_id not in self.accounts[account_id]]):
				self.accounts[account_id][vendor_id] = float(amount)
				self.accounts[account_id]['balance'] -= float(amount)
			else:
				if vendor_id in self.accounts[account_id]:
					logger.info("Allow one hold per vendor id per account , tranaction rejected")
					raise VendorError("Allow one hold per vendor id per account , tranaction rejected")
				elif amount > self.accounts[account_id].get('balance', 0):
					logger.info("Insufficent funds to hold, tranaction rejected")
					raise InsufficentFundError("Insufficent funds to hold, tranaction rejected")
			return self.accounts[account_id]['balance']
		else:
			logger.info("Invalid account number")
			raise InvalidId("Invalid account number")
	
	def settle_hold(self, account_id, vendor_id, actual_amount):
		""" release hold amount and charge actual amount"""
		if all([self.accounts.get(account_id, None), self.accounts.get(account_id, None).get(vendor_id, None)]) :
			self.accounts[account_id]['balance'] += self.accounts[account_id][vendor_id]
			if actual_amount <= self.accounts[account_id].get('balance', 0):
				self.accounts[account_id]['balance'] -= float(actual_amount)
			else:
				logger.info("Insufficent funds, tranaction declined")
				raise InsufficentFundError("Insufficent funds, tranaction declined")
			return 	self.accounts[account_id]['balance']
		
		else:
			logger.info("Invalid account number or vender id")
			raise InvalidId("Invalid account number")
