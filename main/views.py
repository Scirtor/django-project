from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import ItemForm, RegisterForm
from .models import Item
from .serializers import ItemSerializer


def logout_view(request):
    logout(request)
    return redirect("/")


def home(request):
    items = Item.objects.all()
    return render(request, "home.html", {"items": items})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def add_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.save()
            return redirect("/")
    else:
        form = ItemForm()

    return render(request, "add_item.html", {"form": form})


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
