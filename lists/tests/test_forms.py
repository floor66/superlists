from django.test import TestCase

from lists.models import Item, List
from lists.forms import ItemForm

class ItemFormTest(TestCase):
	
	def test_form_renders_item_text_input(self):
		form = ItemForm()
		self.assertIn('placeholder="Enter a To-Do item"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())
		
	def test_form_validation_for_blank_items(self):
		form = ItemForm(data={
			'text': ''
		})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['text'],
			['You can\'t have an empty list item']
		)
		
	def test_form_save_handles_saving_to_a_list(self):
		list_ = List.objects.create()
		form = ItemForm(data={
			'text': 'Save this'	
		})
		item_ = form.save(for_list=list_)
		
		self.assertEqual(item_, Item.objects.all()[0])
		self.assertEqual(item_.text, 'Save this')
		self.assertEqual(item_.list, list_)
		
		
	