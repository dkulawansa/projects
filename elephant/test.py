import unittest
import subprocess
from elephant import (
main,
canvas, 
get_canvas
)

class ElephantTests(unittest.TestCase):
	"""Test class to test elephant.py functionality"""
	def setUp(self):
		canvas(['30', '5'],'test.txt')

	def tearDown(self):
		pass
		
	def test_get_canvas(self):
		res = get_canvas('test.txt')
		self.assertEqual(res, (32, 236, 5))
		
	def test_get_canvas_error(self):
		with self.assertRaises(FileNotFoundError):
			get_canvas('output.txt')
			
	def test_get_canvas_value_error(self):
		f = open('out.txt', 'w')
		with self.assertRaises(ValueError):
			get_canvas('out.txt')
		f.close()
		
if __name__ == '__main__':
	unittest.main()