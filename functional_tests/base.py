from django.test import LiveServerTestCase
from selenium import webdriver
import sys

class FunctionalTest(LiveServerTestCase):
	
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://'+ arg.split('=')[1]
				return
		LiveServerTestCase.setUpClass()
		cls.server_url = cls.live_server_url
		
	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			LiveServerTestCase.tearDownClass()

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()
		
	def list_item_in_list(self, list_item_text):
		todo_list = self.browser.find_element_by_id('todo_list')
		todo_list_items = self.browser.find_elements_by_tag_name('li')
		self.assertIn(list_item_text, [todo_list_item.text for todo_list_item in todo_list_items])

		