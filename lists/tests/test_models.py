from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Item, List

class ListAndItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()
		
		first_item = Item()
		first_item.text = 'First created item'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Second created item'
		second_item.list = list_
		second_item.save()
		
		saved_lists = List.objects.all()
		self.assertEqual(saved_lists.count(), 1)
		self.assertEqual(saved_lists[0], list_)
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		
		self.assertEqual(first_saved_item.text, 'First created item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Second created item')
		self.assertEqual(second_saved_item.list, list_)
		
	def test_cannot_save_empty_list(self):
		list_ = List.objects.create()
		item = Item(list=list_, text='')
		with self.assertRaises(ValidationError):
			item.save()
			
	def test_get_absolute_url(self):
		list_ = List.objects.create()
		self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,))
		
	def test_cannot_save_duplicate_items(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_, text='asd')
		
		with self.assertRaises(ValidationError):
			Item.objects.create(list=list_, text='asd')
			
	def test_CAN_save_same_item_in_different_list(self):
		list1_ = List.objects.create()
		list2_ = List.objects.create()
		Item.objects.create(list=list1_, text='asd')
		Item.objects.create(list=list2_, text='asd') # should _not_ raise ValidationError
		
	def test_list_ordering(self):
		list_ = List.objects.create()
		item1 = Item.objects.create(list=list_, text='one')
		item2 = Item.objects.create(list=list_, text='two')
		item3 = Item.objects.create(list=list_, text='three')
	
		self.assertEqual(
			list(Item.objects.all()),
			[item1, item2, item3]
		)
		