from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Chrome('C:/chromedriver.exe')

	def tearDown(self):
		self.browser.quit()
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		# John needs to maintain a To-Do list.
		# He goes online to a website that provides this feature.
		self.browser.get('http://localhost:8000')
		self.browser.implicitly_wait(3)

		# He sees the words To-Do in the title of his browser so he knows he's in the right place
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# He is greeted by a page where he can immediately add to his To-Do list
		inputbox = self.browser.find_element_by_id('new_todo_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a To-Do item'
		)

		# He types "Buy milk, eggs and flour" into a text box (he wants to bake a cake)
		inputbox.send_keys('Buy milk, eggs and flour')

		# He hits Enter, and immediately a list is shown with:
		# "1: Buy milk, eggs and flour"
		inputbox.send_keys(Keys.ENTER)
		
		todo_list = self.browser.find_element_by_id('todo_list')
		todo_list_items = self.browser.find_elements_by_tag_name('li')
		self.assertTrue(
			any(todo_list_item.text == '1: Buy milk, eggs and flour' for todo_list_item in todo_list_items),
			'New item did not appear in list'
		)

		# There is another text box for another To-Do item
		# He types "Bake cake"
		self.fail('Finish the test!')

		# He hits enter, the page updates, and the item is shown underneath:
		# "2: Bake cake"
		
		# John sees that the website remembers his To-Do list. He has a unique URL that points to his list specifically
		# He visits this URL, it works.

		# Satisfied, he goes to have a beer.
		
	if __name__ == '__main__':
		unittest.main(warnings='ignore')
		
