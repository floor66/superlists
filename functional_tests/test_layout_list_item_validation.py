from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):		

	def test_cannot_add_empty_list_item(self):
		# John goes to the home page and accidentally submits an empty list item.
		
		# Home page refreshes and an error message pops up, notifying him of his mistake.
		
		# He tries again, with text this time.
		
		# He submits an empty list item again.
		
		# There is a similar error.
		
		# He corrects it by filling something in.
		self.fail("Write this test!")
	