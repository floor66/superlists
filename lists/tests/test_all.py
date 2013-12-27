from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

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

class NewItemTest(TestCase):
	
	def test_can_save_POST_to_existing_list(self):
		list_one = List.objects.create()
		list_two = List.objects.create()
		
		self.client.post(
			'/lists/%d/new_item' % (list_one.id,),
			data = {
				'item_text': 'A new item for an existing list'
			}
		)
		
		self.assertEqual(Item.objects.all().count(), 1)
		new_item = Item.objects.all()[0]
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, list_one)
		
	def test_redirects_to_list_view(self):
		list_one = List.objects.create()
		list_two = List.objects.create()
		
		response = self.client.post(
			'/lists/%d/new_item' % (list_one.id,),
			data = {
				'item_text': 'A new item for an existing list'
			}
		)
	
		self.assertRedirects(response, '/lists/%d/' % (list_one.id,))
		