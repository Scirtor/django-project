from django.shortcuts import render, redirect
from .models import Item
from .forms import RegisterForm, ItemForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
def add_item(request, item_id=None):
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


@csrf_exempt
def items_api(request):
    if request.method == 'GET':
        items = list(Item.objects.values(
            'id', 'title', 'description', 'status', 'author_id', 'date'
        ))
        return JsonResponse(items, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)

        item = Item.objects.create(
            title=data['title'],
            description=data['description'],
            status=data['status'],
            author_id=data['author_id']
        )

    if request.method == 'PUT':
        if not item_id:
            return JsonResponse({'error': 'item_id required'}, status=400)

        data = json.loads(request.body)
        item = Item.objects.get(id=item_id)

        item.title = data.get('title', item.title)
        item.description = data.get('description', item.description)
        item.status = data.get('status', item.status)

        item.save()

        return JsonResponse({'id': item.id, 'status': 'created'})