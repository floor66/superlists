from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
	
	def test_can_start_a_list_and_retrieve_it_later(self):
		# John needs to maintain a To-Do list.
		# He goes online to a website that provides this feature.
		self.browser.get(self.server_url)
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
		
		johns_url = self.browser.current_url
		self.assertRegex(johns_url, '/lists/.+')
		self.list_item_in_list('1: Buy milk, eggs and flour')
		
		# There is another text box for another To-Do item
		# He types "Bake cake"
		inputbox = self.browser.find_element_by_id('new_todo_item')
		inputbox.send_keys('Bake cake')

		# He hits enter, the page updates, and the item is shown underneath:
		# "2: Bake cake"
		inputbox.send_keys(Keys.ENTER)
		
		self.list_item_in_list('1: Buy milk, eggs and flour')
		self.list_item_in_list('2: Bake cake')
		
		# A new user visits the site: Jake
		self.browser.quit()
		self.browser = webdriver.Firefox()
		self.browser.get(self.server_url)
		
		page_body = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('milk, eggs', page_body)
		self.assertNotIn('cake', page_body)
		
		# Jake also has a few items he'd like to put on a To-Do list
		inputbox = self.browser.find_element_by_id('new_todo_item')
		inputbox.send_keys('Pickup kids after work')
		inputbox.send_keys(Keys.ENTER)
		
		# Jake has his own, personal list (read: URL)
		jakes_url = self.browser.current_url
		self.assertRegex(jakes_url, 'lists/.+')
		self.assertNotEqual(johns_url, jakes_url)
		
		page_body = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('milk, eggs', page_body)
		self.assertIn('kids', page_body)
		
		# Jake is happy now. He goes to sleep
	
