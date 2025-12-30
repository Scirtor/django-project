from django.shortcuts import render, redirect
from .models import Item
from .forms import RegisterForm, ItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/')

def home(request):
    items = Item.objects.all().order_by('-date')
    return render(request, 'home.html', {'items': items})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def add_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.save()
            return redirect('/')
    else:
        form = ItemForm()

    return render(request, 'add_item.html', {'form': form})
