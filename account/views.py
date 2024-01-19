from django.shortcuts import render,redirect
from  .forms import UserRegistrationForm,UserUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserAccount
from django.contrib.auth import login,logout
from django.views.generic import FormView
from django.views.generic import ListView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView,PasswordChangeView
from transaction.models import Transaction
from django.contrib.auth.models import User
# Create your views here.
class UserRegistrationView(FormView):
    template_name= "register.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy('register')

    def form_valid(self, form):
        user=form.save() #save method call
        
        login(self.request,user) 
        messages.success(self.request, "Registration successfull")

        print(user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context   

class UserLoginView(LoginView):
    template_name='register.html'
    def get_success_url(self):
        return reverse_lazy('homepage')

    def form_valid(self, form):
        messages.success(self.request, "Logged in Successful")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, "Please Enter valid information")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['type'] = 'Log In'
          return context           

# class UserLogoutView(LogoutView):
#     def get_success_url(self):
#         if self.request.user.is_authenticated:
#             logout(self.request)
#         return reverse_lazy('homepage')
         
@login_required
def user_logout(request):
    if request.user.is_authenticated:
            logout(request)
    return redirect('homepage')   


class  ProfileView(LoginRequiredMixin,ListView):
      template_name ='profile.html'
      model=Transaction

      def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user.account
        )

        def get_context_data(self,**kwargs):
          context = super().get_context_data(**kwargs)
          context['object'] =self.request.user
          context['account']=self.request.user.account
          return context


class EditProfileView(LoginRequiredMixin,UpdateView):
    template_name='register.html'
    model=User
    form_class =UserUpdateForm

    context_object_name = 'user_data' # Change the context object name
    def get_success_url(self):
        return reverse_lazy('profile_detail')

    def get_object(self):
        return self.request.user
#    currebtly user object fetch

    def form_valid(self, form):
        messages.success(self.request, "Profile Updated Successful")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, "Please Enter valid information")
        return super().form_invalid(form)    

    def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['type'] = 'Update Profile'
         
          return context                  