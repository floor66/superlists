from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List
from django.utils.html import escape

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

class ListViewTest(TestCase):

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

class NewListTest(TestCase):
	
	def test_can_POST(self):
		self.client.post(
			'/lists/new',
			data = {
				'item_text': 'A new list item'
			}
		)
		
		self.assertEqual(Item.objects.all().count(), 1)
		new_item = Item.objects.all()[0]
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data = {
				'item_text': 'A new list item'
			}
		)
		
		new_list = List.objects.all()[0]
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
		
	def test_validation_errors_sent_back_to_home_page_template(self):
		response = self.client.post('/lists/new',
			data = {
				'item_text': ''
			}
		)

		self.assertEqual(Item.objects.all().count(), 0)
		self.assertTemplateUsed(response, 'home.html')
		expected_error = escape('You can\'t have an empty list item')
		self.assertContains(response, expected_error)

	def test_can_save_POST_to_existing_list(self):
		list_one = List.objects.create()
		list_two = List.objects.create()
		
		self.client.post(
			'/lists/%d/' % (list_one.id,),
			data = {
				'item_text': 'A new item for an existing list'
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
				'item_text': 'A new item for an existing list'
			}
		)
	
		self.assertRedirects(response, '/lists/%d/' % (list_one.id,))
		