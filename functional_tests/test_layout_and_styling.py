from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):
	
	def test_layout_and_styling(self):
		# John goes to the home page
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024, 768)
		
		# He notices how the input box is nicely centered
		inputbox = self.browser.find_element_by_id('new_todo_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=25
		)
		
		# He starts a new list and notices the centered box in the list page as well
		inputbox.send_keys('testing the list\n')
		inputbox = self.browser.find_element_by_id('new_todo_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=25
		)
