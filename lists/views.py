from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.views.generic import FormView, CreateView

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm

# Create your views here.
class HomePageView(FormView):
	template_name = 'home.html'
	form_class = ItemForm

class ViewAndAddToListView(CreateView):
	template_name = 'list.html'
	model = List
	form_class = ExistingListItemForm
	
	def get_form(self, form_class):
		self.object = self.get_object()
		return form_class(for_list=self.object, data=self.request.POST)
	
def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	form = ExistingListItemForm(for_list=list_, data=request.POST or None)
	
	if form.is_valid():
		form.save()
		return redirect(list_)
	
	return render(request, 'list.html', {
		'list': list_,
		'form': form
	})

class NewListView(CreateView, HomePageView):

	def form_valid(self, form):
		list_ = List.objects.create()
		Item.objects.create(text=form.cleaned_data['text'], list=list_)
		return redirect(list_)
	
