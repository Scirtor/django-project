from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import markdown

# Create your models here.

class Post(models.Model):
    """Model for blog posts and CTF writeups"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField(help_text="Markdown content for the post")
    excerpt = models.TextField(max_length=500, blank=True, help_text="Short description of the post")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    category = models.CharField(max_length=100, default='General', 
                               help_text="Category like 'CTF Writeup', 'Blog Post', etc.")
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def get_html_content(self):
        """Convert Markdown content to HTML"""
        md = markdown.Markdown(extensions=[
            'extra',
            'codehilite',
            'toc',
        ])
        return md.convert(self.content)

