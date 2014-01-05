from django.test import TestCase

from lists.models import Item, List
from lists.forms import (
	EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR,
	ItemForm, ExistingListItemForm
)

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
			[EMPTY_LIST_ERROR]
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
		
class ExistingListItemFormTest(TestCase):

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
			[EMPTY_LIST_ERROR]
		)
		
	def test_form_validation_for_duplicate_items(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='no doubles')
		form = ExistingListItemForm(for_list=list_, data={
			'text': 'no doubles'
		})
		

		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['text'],
			[DUPLICATE_ITEM_ERROR]
		)
		
	def test_form_save(self):
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_, data={
			'text': 'testing!'
		})
		item_ = form.save()
		
		self.assertEqual(item_, Item.objects.all()[0])
