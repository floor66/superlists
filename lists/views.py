from django.shortcuts import render, redirect
from lists.models import Item

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def view_list(request):
	return render(request, 'list.html', {
		'items': Item.objects.all()
	})

def new_list(request):
	item = Item.objects.create(text=request.POST['item_text'])
	return redirect('/lists/only-one-list/')
	
