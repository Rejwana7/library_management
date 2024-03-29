from django.shortcuts import render
from categories.models import Category
from book.models import Book
from django.views.generic import ListView


# Create your views here
class Homeview(ListView):
    model=Book
    template_name='home.html'
    context_object_name='data'
    
    def get_queryset(self):
        category_slug=self.kwargs.get('category_slug')

        if category_slug:
            category=Category.objects.get(slug=category_slug)
            return Book.objects.filter(category=category)

        return Book.objects.all()  

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['book'] = Book.objects.all()
        return context   