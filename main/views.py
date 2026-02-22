from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.db.models import Q
from django.urls import reverse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import ItemForm, RegisterForm, CommentForm
from .models import Item, Comment
from .serializers import ItemSerializer, CommentSerializer


def logout_view(request):
    logout(request)
    return redirect("home")


def home(request):
    search_query = request.GET.get("q", "")

    items = Item.objects.all()

    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    context = {
        "items": items,
        "search_query": search_query,
    }

    return render(request, "home.html", context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def add_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.save()
            return redirect("home")
    else:
        form = ItemForm()

    return render(request, "add_item.html", {"form": form})


@login_required
def add_comment(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return redirect("home")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.item = item
            comment.author = request.user
            comment.save()
            # Редирект с параметром для автоматического открытия модального окна
            return redirect(f"{reverse('home')}?open_modal={item_id}")
    else:
        form = CommentForm()

    return redirect("home")


@login_required
def delete_item(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return redirect("home")

    # Check if the user is the author of the item
    if request.user != item.author:
        return redirect("home")

    if request.method == "POST":
        item.delete()
        return redirect("home")

    return redirect("home")


@login_required
def edit_item(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return redirect("home")

    # Check if the user is the author of the item
    if request.user != item.author:
        return redirect("home")

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ItemForm(instance=item)

    return render(request, "edit_item.html", {"form": form, "item": item})


@api_view(["GET", "POST"])
def items_api(request):
    if request.method == "GET":
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def item_detail_api(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def item_comments_api(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        comments = Comment.objects.filter(item=item)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # POST - создание нового комментария
    if not request.user.is_authenticated:
        return Response(
            {"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED
        )

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(item=item, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
