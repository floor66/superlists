from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_LIST_ERROR

# Create your views here.
def home_page(request):
	return render(request, 'home.html', {
		'form': ItemForm()
	})

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	form = ItemForm(data=request.POST or None)
	
	if form.is_valid():
		try:
			form.save(for_list=list_)
			return redirect(list_)
		except ValidationError:
			form.errors.update({'text': 'You\'ve already got this in your list'})
	
	return render(request, 'list.html', {
		'list': list_,
		'form': form
	})

def new_list(request):
	form = ItemForm(data=request.POST)
	
	if form.is_valid():
		list_ = List.objects.create()
		form.save(for_list=list_)
		return redirect(list_)
	else:
		return render(request, 'home.html', {
			'form': form
		})

