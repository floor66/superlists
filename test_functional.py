from selenium import webdriver
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
		self.fail('Finish the test!')

		# He is greeted by a page where he can immediately add to his To-Do list

		# He types "Buy milk, eggs and flour" into a text box (he wants to bake a cake)

		# He hits Enter, and immediately a list is shown with:
		# "1: Buy milk, eggs and flour"

		# There is another text box for another To-Do item
		# He types "Bake cake"

		# He hits enter, the page updates, and the item is shown underneath:
		# "2: Bake cake"
		
		# John sees that the website remembers his To-Do list. He has a unique URL that points to his list specifically
		# He visits this URL, it works.

		# Satisfied, he goes to have a beer.
		
	if __name__ == '__main__':
		unittest.main(warnings='ignore')
		
