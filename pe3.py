from datetime import date
from sys import stderr
import string

_ltrlist = list(string.ascii_lowercase)
_num2ltr = dict(zip(range(26), list(_ltrlist)))
_ltr2num = dict(zip(list(_ltrlist), range(26)))

def _encode_chr(input_chr, shift):
  if input_chr >= 'a' and input_chr <= 'z':
    return _num2ltr[(_ltr2num[input_chr] + shift) % 26]
  elif input_chr >= 'A' and input_chr <= 'Z':
    return _num2ltr[(_ltr2num[input_chr.lower()] + shift) % 26]
  else:
    return input_chr

def encode(input_text, shift):
  output_text = ''
  for c in input_text:
    output_text += _encode_chr(c, shift)
  return (_ltrlist, output_text)

def decode(input_text, shift):
  output_text = ''
  for c in input_text:
    output_text += _encode_chr(c, -1*shift)
  return output_text

class BankAccount:
  def __init__(self, name='Rainy', ID='1234', creation_date=date.today(), balance=0):
    self.name = name
    self.ID = ID
    self._creation_date = None
    self.creation_date = creation_date
    self._balance = None
    self.balance = balance

  def _err(self, msg):
    print(msg, file=stderr)
  
  @property
  def creation_date(self):
    return self._creation_date
  
  @creation_date.setter
  def creation_date(self, value):
    if isinstance(value, tuple) and len(value) == 3:
      value = date(value[0], value[1], value[2])
    if value <= date.today():
      self._creation_date = value
      return
    raise Exception("creation_date must be of type datetime.date and represent a date not after the current date.")
  
  @property
  def balance(self):
    return self._balance
  
  @balance.setter
  def balance(self, value):
    self._balance = value
  
  def view_balance(self):
    print(f"Current balance: {self.balance}")

  def deposit(self, amount):
    if amount < 0:
      self._err("deposit amount may not be negative")
      return
    self.balance += amount
    self.view_balance()
  
  def withdraw(self, amount):
    if amount < 0:
      self._err("withdrawal amount may not be negative")
      return
    self.balance -= amount
    self.view_balance()

class SavingsAccount(BankAccount):
  def __init__(self, name='Rainy', ID='1234', creation_date=date.today(), balance=0):
    super().__init__(name, ID, creation_date, balance)

  def withdraw(self, amount):
    if (date.today() - self.creation_date).days < 180:
      self._err("withdrawals are only permitted after the account has been in existence for 180 days")
      return
    return super().withdraw(amount)
  
  @property
  def balance(self):
    return self._balance

  @balance.setter
  def balance(self, value):
    if value < 0:
      self._err("savings accounts do not permit overdrafts")
      return
    self._balance = value

class CheckingAccount(BankAccount):
  def __init__(self, name='Rainy', ID='1234', creation_date=date.today(), balance=0):
    super().__init__(name, ID, creation_date, balance)

  def withdraw(self, amount):
    if self.balance - amount < 0:
      amount += 30
      self._err("withdrawal resulting in overdraft incurs a $30 penalty in checking accounts")
    return super().withdraw(amount)