from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import (
	DUPLICATE_ITEM_ERROR, EMPTY_LIST_ERROR,
	ExistingListItemForm, ItemForm
)

class HomePageTest(TestCase):

	def test_home_page_renders_correct_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')
		
	def test_home_page_uses_item_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'], ItemForm)

class ListViewTest(TestCase):
	
	def post_invalid_input(self):
		list_ = List.objects.create()
		
		return self.client.post(
			'/lists/%d/' % (list_.id,),
			data = {
				'text': ''
			}
		)
	
	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertTemplateUsed(response, 'list.html')

	def test_shows_all_items(self):
		list_ = List.objects.create()
		Item.objects.create(text='item1', list=list_)
		Item.objects.create(text='item2', list=list_)
		
		list2_ = List.objects.create()
		Item.objects.create(text='item2.1', list=list2_)
		Item.objects.create(text='item2.2', list=list2_)
		
		response = self.client.get('/lists/%d/' % (list_.id,))
		
		self.assertContains(response, 'item1')
		self.assertContains(response, 'item2')
		self.assertNotContains(response, 'item2.1')
		self.assertNotContains(response, 'item2.2')
		
	def test_passes_correct_list_id(self):
		list_one = List.objects.create()
		list_two = List.objects.create()
		
		response = self.client.get('/lists/%d/' % (list_one.id,))
		
		self.assertEqual(response.context['list'], list_one)
		
	def test_displays_item_form(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id,))
		self.assertIsInstance(response.context['form'], ExistingListItemForm)
		self.assertContains(response, 'name="text"')
		
	def test_invalid_input_means_no_db_changes(self):
		self.post_invalid_input()
		self.assertEqual(Item.objects.all().count(), 0)
		
	def test_invalid_input_renders_list_template(self):
		response = self.post_invalid_input()
		self.assertTemplateUsed(response, 'list.html')
		
	def test_invalid_input_renders_form_with_errors(self):
		response = self.post_invalid_input()
		self.assertIsInstance(response.context['form'], ExistingListItemForm)
		self.assertContains(response, escape(EMPTY_LIST_ERROR))
		
	def test_duplicate_item_validation_error_ends_up_on_lists_page(self):
		list_ = List.objects.create()
		item_ = Item.objects.create(list=list_, text='asd')
		response = self.client.post(
			'/lists/%d/' % (list_.id,),
			data = {
				'text': 'asd'
			}
		)
		
		expected_error = escape(DUPLICATE_ITEM_ERROR)
		self.assertContains(response, expected_error)
		self.assertTemplateUsed(response, 'list.html')
		self.assertEqual(Item.objects.all().count(), 1)

class NewListTest(TestCase):
	
	def test_can_POST(self):
		self.client.post(
			'/lists/new',
			data = {
				'text': 'A new list item'
			}
		)
		
		self.assertEqual(Item.objects.all().count(), 1)
		new_item = Item.objects.all()[0]
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data = {
				'text': 'A new list item'
			}
		)
		
		new_list = List.objects.all()[0]
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
		
	def test_validation_errors_sent_back_to_home_page_template(self):
		response = self.client.post('/lists/new',
			data = {
				'text': ''
			}
		)

		self.assertEqual(List.objects.all().count(), 0)
		self.assertEqual(Item.objects.all().count(), 0)
		self.assertTemplateUsed(response, 'home.html')
		self.assertContains(response, escape(EMPTY_LIST_ERROR))
		self.assertIsInstance(response.context['form'], ItemForm)

	def test_can_save_POST_to_existing_list(self):
		list_one = List.objects.create()
		list_two = List.objects.create()
		
		self.client.post(
			'/lists/%d/' % (list_one.id,),
			data = {
				'text': 'A new item for an existing list'
			}
		)
		
		self.assertEqual(Item.objects.all().count(), 1)
		new_item = Item.objects.all()[0]
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, list_one)
		
	def test_POST_redirects_to_list_view(self):
		list_one = List.objects.create()
		list_two = List.objects.create()
		
		response = self.client.post(
			'/lists/%d/' % (list_one.id,),
			data = {
				'text': 'A new item for an existing list'
			}
		)
	
		self.assertRedirects(response, '/lists/%d/' % (list_one.id,))
		