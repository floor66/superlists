from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item

class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get('/lists/only-one-list/')
		self.assertTemplateUsed(response, 'list.html')

	def test_shows_all_items(self):
		Item.objects.create(text='item1')
		Item.objects.create(text='item2')
		
		response = self.client.get('/lists/only-one-list/')
		
		self.assertContains(response, 'item1')
		self.assertContains(response, 'item2')

class ItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'First created item'
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Second created item'
		second_item.save()
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		
		self.assertEqual(first_saved_item.text, 'First created item')
		self.assertEqual(second_saved_item.text, 'Second created item')

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
		
	def test_home_page_can_POST(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		
		response = home_page(request)
		
		self.assertEqual(Item.objects.all().count(), 1)
		new_item = Item.objects.all()[0]
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_home_page_redirects(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		
		response = home_page(request)
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/lists/only-one-list/')
		
	def test_home_page_only_saves_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.all().count(), 0)
