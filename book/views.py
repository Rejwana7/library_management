
from django.shortcuts import render,redirect

from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserAccount
from django.contrib.auth import login,logout
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from . import forms
from django.views.generic import DetailView
from  .models import Book
from transaction.models import Transaction
from django.urls import reverse_lazy
# Create your views here.


class BookDetailView(DetailView):
    model=Book
    template_name ='details.html'
    context_object_name = 'book'

    # pk_url_kwarg = 'id'

    def post(self,request,*args,**kwargs):
        book=self.get_object()
        if self.request.method=="POST": 
            comment_form=forms.CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment=comment_form.save(commit=False)
                new_comment.book=book
                new_comment.user= self.request.user
                new_comment.save()
            return self.get(request, *args,**kwargs)  
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        book=self.object
        comments=book.comments.all()
        comment_form=forms.CommentForm()
        context['comments']=comments
        context['comment_form'] = comment_form
        try:
            user_has_borrowed= Transaction.objects.filter(book=book,user=self.request.user.account).exists()
        except:
            user_has_borrowed= False    
        context['user_has_borrowed'] =user_has_borrowed
        return context