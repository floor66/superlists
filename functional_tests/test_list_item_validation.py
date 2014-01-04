from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):		

	def test_cannot_add_empty_list_item(self):
		# John goes to the home page and accidentally submits an empty list item.
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('\n')
		
		# Home page refreshes and an error message pops up, notifying him of his mistake.
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, 'You can\'t have an empty list item')
		
		# He tries again, with text this time.
		self.get_item_input_box().send_keys('Buy cookies for milk\n')
		self.list_item_in_list('1: Buy cookies for milk')
		
		# He submits an empty list item again.
		self.list_item_in_list('1: Buy cookies for milk')
		self.get_item_input_box().send_keys('\n')
		
		# There is a similar error.
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, 'You can\'t have an empty list item')

		# He corrects it by filling something in.
		self.get_item_input_box().send_keys('Pre-heat milk for 1.5 minutes\n')
		self.list_item_in_list('1: Buy cookies for milk')
		self.list_item_in_list('2: Pre-heat milk for 1.5 minutes')
		
	