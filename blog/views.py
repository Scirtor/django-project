from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.

class PostListView(ListView):
    """View to list all published posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get unique categories
        context['categories'] = Post.objects.filter(published=True).values_list('category', flat=True).distinct()
        return context


class PostDetailView(DetailView):
    """View to display a single post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(published=True)


class CategoryListView(ListView):
    """View to list posts by category"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        category = self.kwargs.get('category')
        return Post.objects.filter(published=True, category=category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Post.objects.filter(published=True).values_list('category', flat=True).distinct()
        context['current_category'] = self.kwargs.get('category')
        return context

